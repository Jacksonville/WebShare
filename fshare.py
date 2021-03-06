import bottle
import argparse
import os
import socket
import logging

logging.basicConfig(level=logging.DEBUG)
bottle.TEMPLATE_PATH.append('./static/templates')
appPath = os.path.split(os.path.abspath(__file__))[0]

def get_port(min_port=8000, max_port=9000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(min_port, max_port):
        if port > max_port:
            raise IOError('Could not find a free port between {0} and {1}'.format(min_port, max_port))
        try:
            s.bind(('0.0.0.0', port))
            return port
        except socket.error as error:
            continue

def populate_clipboard(text):
    from sys import platform
    if platform == "linux" or platform == "linux2":
        import gtk
        clipboard = gtk.clipboard_get()
        clipboard.set_text(text.strip())
        clipboard.store()
    elif platform == "darwin":
        os.system("echo '%s' | pbcopy" % text)
    elif platform == "win32":
        os.system("echo '%s' | clip" % text)

class WebServer(object):
    def __init__(self, directory):
        self.directory = directory

    def __new__(cls, *args, **kwargs):
        obj = super(WebServer, cls).__new__(cls, *args, **kwargs)
        bottle.route('/static/:path/:file#.*#')(obj.get_static_files)
        bottle.route("/")(obj.render_directory)
        bottle.route("/dl")(obj.download_file)
        return obj

    def list_dir(self, directory):
        filelist = [x for x in os.listdir(directory) if os.path.isfile(os.path.join(directory, x))]
        dirlist = [x for x in os.listdir(directory) if os.path.isdir(os.path.join(directory, x))]
        return dirlist, filelist

    def get_static_files(self, file, path):
        return bottle.static_file(file, root=os.path.join(appPath,'static',path))

    def render_directory(self):
        ldir = os.path.join(self.directory, bottle.request.GET.get('dir','/')[1:])
        dirlist, filelist = self.list_dir(ldir)
        if ldir != self.directory:
            ldir = '/'+ldir.split(self.directory)[1]+'/'
        else:
            ldir = '/'
        return bottle.template('index',
                               curr_dir=ldir,
                               dirlist=dirlist,
                               filelist=filelist)

    def download_file(self):
        filename = bottle.request.GET.get('filename')
        return bottle.static_file(filename, root=self.directory, download=filename)

def main():
    parser = argparse.ArgumentParser(description='Quickly share files via web browser')
    parser.add_argument('path',
                        help='directory that you would like to share')
    args = parser.parse_args()
    port = get_port()
    directory = args.path
    obj = WebServer(directory)
    app = bottle.app()
    url = 'http://'+socket.gethostbyname(socket.gethostname())+':'+str(port)
    populate_clipboard(url)
    logging.info('%s copied to your clipboard' % url)
    bottle.run(app=app, host='0.0.0.0', port=int(port))

if __name__ == '__main__':
    main()
