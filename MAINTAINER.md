# Create new package

You should be member of the group pywebdriver / admin users on github.

```bash
git checkout origin master
git pull origin master
# bump version in file `./VERSION`
# bump version in file `./windows/setup.iss`
git commit -am "[BUMP] vX.Y.Z"
git tag vX.Y.Z
git push origin vX.Y.Z
git push origin master
```
