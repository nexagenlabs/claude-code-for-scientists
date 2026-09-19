# site/

The companion site at science.nexagenlabs.com.

`build_site.py` reads the repository and writes `site/dist/`. The build list,
the chapter titles and the printed addresses all come from `builds/` and
`CHAPTERS.md`, so the site cannot claim a build that does not exist.

```
python site/build_site.py
```

Netlify runs the same command on every push to `main` and publishes
`site/dist/`. `site/dist/` is generated, so it is not committed.

The output is self contained: no fonts, scripts or styles are fetched from
anywhere, which is why the content security policy in `netlify.toml` can deny
everything except the page's own inline style.
