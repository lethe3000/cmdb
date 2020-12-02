import re
if __name__ == '__main__':
    import requests
    resp = requests.get('https://git.ops.yunlizhi.cn/api/v4/projects/212/jobs/24361/trace', headers={'PRIVATE-TOKEN': 'P58dMHVjbyiiiiwkTozp'})
    text = resp.text
    print(re.search('^(?P<image>[-a-zA-Z0-9:/.]*) build success$', text, re.MULTILINE).groupdict())
    print('done')
