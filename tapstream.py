import shutil
from optparse import OptionParser
import requests
import re
import sys
from requests.exceptions import ConnectionError, HTTPError, Timeout


prefix='media_w1122970213_b862904_'
outfilename='ek1.ts'

ts_list=[ prefix + str(i) + '.ts' for i in range(1, 122)]

def cat_ts_files(outfilename, ts_list):
	with open(outfilename, 'wb') as outfile:
	    for filename in tslist:
	        print 'appending file ' + filename
	        with open(filename, 'rb') as readfile:
	            shutil.copyfileobj(readfile, outfile)

def breakdown_ts_url(url):
	ts_re = re.compile('(.*_)([\d]*).ts')
	m = ts_re.match(url)
	if m:
		prefix = m.group(1)
		start_index = int(m.group(2))
		print 'url prefix='+prefix
		print 'start index='+str(start_index)
		return prefix, start_index
	raise Exception('Cannot decode url:' + url)

def download_ts(output, prefix, start_index):
	index = start_index
	print 'downloading ' + prefix
        total_len = 0
        print 'Downloading...'
        timeouts = 0

	with open(output, 'wb') as dest:
		while 1:
			url = prefix + str(index) + '.ts'
                        try:
			        r = requests.get(url, timeout=30)
                        except (Timeout, ConnectionError):
                                timeouts += 1
			        print '\r   %s MB - Timed out! Retrying...' % format(total_len/(1024*1024), ',d'),
                                continue
			if r.status_code == requests.codes.ok:
                                total_len += len(r.content)
			        print '\r   %s MB...' % format(total_len/(1024*1024), ',d'),
                                sys.stdout.flush()
				dest.write(r.content)
				index += 1
			else:
				break

        print
	print 'Done'
        if timeouts:
               print('Timeouts: %d' % timeouts)


def main():
    parser = OptionParser(usage="usage: %prog [options] [<run-name>]")

    parser.add_option('-u', '--url', dest='url',
                      action='store',
                      help='first ts file url (e.g. "http://go.streamer.com:1935/encoded_streams/130/117.w1093_b772666_1.ts")',
					  metavar='<ts file url>')

    parser.add_option('-o', '--output', dest='output',
                      action='store',
                      help='output file name without extension (e.g. "test finale")',
					  metavar='<output>')

    (options, args) = parser.parse_args()
    print options
    prefix, start_index = breakdown_ts_url(options.url)
    download_ts(options.output + '.mp4', prefix, start_index)


if __name__ == '__main__':
	main()
