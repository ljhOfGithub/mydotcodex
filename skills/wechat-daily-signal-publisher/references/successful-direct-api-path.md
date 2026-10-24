# Successful WeChat direct API path

Use this path for `/Users/jackie/Documents/mediePlatform`.

## Confirmed sequence

1. Keep Clash Verge in `rule` mode and put the WeChat `DIRECT` domain rules before general proxy rules. TUN can remain enabled.
2. Run the CLI through `../scripts/run-wechat-direct.sh`. The wrapper removes inherited proxy variables and temporarily selects `rule` mode when necessary; it does not disable TUN or force all traffic direct.
   - User-directed fallback: if the `9223` publishing path is unavailable and the user has required Clash to be skipped, set `WECHAT_SKIP_CLASH=1`. The wrapper then avoids the Clash socket entirely while still removing proxy variables from the child command.
3. Require `node src/cli.js token` to return a valid `expires_in`.
4. Run `upload-thumb --file <cover> --send` and record the returned `media_id`.
5. Run `draft:add` or `draft:update` with `--html --author 白Yu观测 --send`.
6. Count a draft only after the API returns its `media_id`.

The 2026-07-23 successful run followed this sequence: Clash changed from `global` to `rule`, explicit WeChat `DIRECT` rules were loaded, WeChat reported the new direct public IP, and the user added that IP to the official-account whitelist. Only after the whitelist update did token retrieval return `expires_in`; permanent cover upload and the draft API then returned media IDs.

## Failure classification

- Proxy variables present: use the wrapper.
- Clash Verge TUN is active: this is valid when the controller is in `rule` mode and WeChat domains match `DIRECT`.
- Another virtual/fake-IP gateway is active: verify its direct-routing state; do not loop API retries while the route remains intercepted.
- Verified WeChat `DIRECT` route returns `40164` with a new public IP: update the WeChat whitelist with that direct IP, then retry token.
- Token succeeds but media/draft fails: record the exact endpoint and platform error without exposing credentials.

Never call `publish:submit` when the run is draft-only.
