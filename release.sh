mv .travis.yml .travis_normal.yml
cp .travis_release.yml .travis.yml
git add .travis.yml
git commit -m "making release"
git push origin master

mv .travis_normal.yml .travis.yml
git add .travis.yml
git commit -m "re-adding tests"
git push origin master
