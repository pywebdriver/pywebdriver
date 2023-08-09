# Create new package

```bash
git checkout origin master
git pull origin master
# bump version in file `./VERSION`
# bump version in file `./windows/setup.iss`
git commit -am "[BUMP] vX.Y.Z"
git tag vX.Y.Z
git push --tags
git push origin master
```
