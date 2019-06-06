import itertools


class Package(object):

    def __init__(self, name, packages, stage):
        self.name = name
        self.packages = packages
        self.stage = stage

    @property
    def info(self):
        return {'name': self.name}

    def urls(self, releases):
        return releases[list(releases.keys())[-1]]

    def _package(self, package):
        filename = package['filename']
        return {
            'filename': filename,
            'url': f'{self.stage}/packages/{filename}'
        }

    def releases(self):
        sorted_packages = sorted(self.packages['Items'], key=lambda p: p['version'])
        groups = itertools.groupby(sorted_packages, key=lambda p: p['version'])
        return {version: [self._package(package) for package in packages] for version, packages in groups}

    def serialize(self):
        releases = self.releases()
        return {'info': self.info, 'last_serial': None, 'releases': releases, 'urls': self.urls(releases)}
