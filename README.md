# JBrowse Chat Server

Provides the backend for coordinating JBrowse chat. Once you have a OAuth client id/secret, you can run with:

```console
$ gunicorn \
	--bind 0.0.0.0:5000 \
	-e SCRIPT_NAME=/test \
	-e GOOGLE_CLIENT_ID='...' \
	-e GOOGLE_CLIENT_SECRET='...' \
	--log-level debug \
	--worker-class eventlet \
	--reload \
	chat:app
```


## LICENSE

AGPL-3.0
