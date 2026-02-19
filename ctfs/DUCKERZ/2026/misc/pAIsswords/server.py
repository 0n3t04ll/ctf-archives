SCRAMBLE_GAIN = 60.0
SEED_SCALE = 2.0
GAIN = 250.0


class PasswordNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 24)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_poly = torch.cat([x, x.pow(2)], dim=1)
        x = torch.tanh(self.fc1(x_poly))
        x = torch.tanh(self.fc2(x))
        return self.fc3(x)


def get_password(seed: torch.Tensor) -> torch.Tensor:

    with torch.no_grad():
        norm_seed = (seed - TARGET_SEED) / SEED_SCALE
        inp = norm_seed.view(1, -1)
        raw = password_net(inp).squeeze(0)
        delta = raw - origin_baked
        base = origin_baked + GAIN * delta

        diff = seed - TARGET_SEED
        diff_mag = diff.abs().item()
        if diff_mag != 0.0:
            idx = torch.arange(1, 25, dtype=torch.float32)
            seed_scalar = float(seed.item())
            noise = torch.sin(idx * (0.73 * seed_scalar)) + torch.cos(idx * (1.21 * seed_scalar))
            noise = noise / (noise.norm() + 1e-6)
            base = base + SCRAMBLE_GAIN * diff_mag * noise
        return base


@app.route("/generate", methods=["POST"])
def generate() -> tuple:
    data = request.get_json(silent=True)
    seed, err = safe_seed(data)
    if err:
        return err

    if abs(seed.item() - TARGET_SEED.item()) < 0.8:
        return jsonify({"error": "FORBIDDEN SEED RANGE"}), 403

    pwd_vec = get_password(seed)
    return jsonify(
        {
            "parsed_seed": seed.tolist(),
            "password_vector": pwd_vec.tolist(),
            "password_string": vector_to_ascii(pwd_vec),
        }
    )
