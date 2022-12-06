# Pomerium Vault Access
This is a small wrapper that allows you to access Hashicorp Vault behind a Pomerium auth proxy.

Assumes that you have `vault` installed in your working path.

"pv" = pomerium -> vault

# Installation

```
sudo -H pip3 install requests
cat main.py | sed  -e 's/{{VAULT_ADDR}}/your.vault.address.com/g' > vlogin
chmod +x vlogin
sudo mv vlogin /usr/local/bin/vlogin
```

# Usage

Put this function in your .bashrc file:

```bash
pv() { vault $1 -header "Authorization=Pomerium $(cat ~/.pomerium_jwt)"; }
```

Restart your terminal or
```bash
source ~/.bashrc
```

Then use as normal:

```bash
# login at the beginning of your session
pvlogin

# use 'pv' in-place of 'vault'
export VAULT_TOKEN=hvc.123.abc
pv status
pv kv get kv/test
... etc ...
```
