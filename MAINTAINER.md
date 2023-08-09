# Create new package

- bump version in file `./VERSION`
- bump version in file `./windows/setup.iss`

```bash
git checkout origin master
git commit -am "[BUMP] vX.Y.Z"
git tag vX.Y.Z
git push --tags
git push origin master
```
