const express = require('express');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.set('view cache', false);
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const workspaces = {};

function deepMerge(target, source) {
    for (const key in source) {
        if (key === '__proto__') continue;

        if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
            if (target[key] == null) {
                target[key] = {};
            }
            deepMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

app.get('/', (req, res) => {
    res.render('index', { workspaceIds: Object.keys(workspaces) });
});

app.post('/api/workspace', (req, res) => {
    const { id, settings } = req.body;
    if (!id || typeof id !== 'string') {
        return res.status(400).json({ error: 'Missing or invalid workspace id' });
    }
    if (!settings || typeof settings !== 'object') {
        return res.status(400).json({ error: 'Missing or invalid settings object' });
    }
    if (!workspaces[id]) workspaces[id] = {};
    deepMerge(workspaces[id], settings);
    res.json({ success: true, workspace: workspaces[id] });
});

app.get('/api/workspace/:id', (req, res) => {
    const id = req.params.id;
    const workspace = workspaces[id];
    if (!workspace) {
        return res.status(404).json({ error: 'Workspace not found' });
    }
    res.render('workspace', { workspace, id });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Hive running on port ${PORT}`);
});
