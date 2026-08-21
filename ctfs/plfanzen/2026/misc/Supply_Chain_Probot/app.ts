// I used Deno for some reason, idk
// Node is boring I guess
import { Probot } from "jsr:@probot/bot";

export default (app: Probot) => {
  app.on("issues.opened", async (context) => {
    if (
      context.payload.sender.login === "plfanzen-ctf-instancer[bot]" &&
      context.payload.repository.private
    ) {
      if (context.payload.issue.body == "/flag") {
        await context.octokit.rest.issues.createComment(
          context.issue({
            body: `The flag is: pflanzen{redacted}`,
          }),
        );
      }
    }
  });
};
