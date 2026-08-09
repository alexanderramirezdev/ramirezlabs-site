# ramirezlabs.app

Source for the Ramirez Labs site. Plain HTML, no build step, no framework.

```
index.html studio landing page
cairnskin/
 index.html support page
 privacy.html privacy policy
```

## Deploying

Connected to Cloudflare Pages. Pushing to `main` deploys automatically.

Build settings: no build command, output directory `/`.

## Adding an app

Create a folder named after the app containing `index.html` (support) and
`privacy.html`. App Store Connect requires a reachable URL for both before
a submission can go through.
