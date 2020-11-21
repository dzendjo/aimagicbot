import logging
import os

import callbacks
import commands
import keyboards
import mybot
import rocketgram
import statistics
import unknown


import data
from templates import templates

import j2tools
import jinja2
import jinja2.ext


# avoid to remove "unused" imports by optimizers
def fix_imports():
    _ = callbacks
    _ = commands
    _ = keyboards
    _ = statistics
    _ = unknown


logger = logging.getLogger('minibots.engine')


def main():
    mode = os.environ.get('MODE')
    if mode is None and 'DYNO' in os.environ:
        mode = 'heroku'

    if mode not in ('updates', 'webhook', 'heroku'):
        raise TypeError('MODE must be `updates` or `webhook` or `heroku`!')

    logging.basicConfig(format='%(asctime)s - %(levelname)-5s - %(name)-30s: %(message)s')
    logging.basicConfig(level=logging.ERROR)
    logging.getLogger('engine').setLevel(logging.INFO)
    logging.getLogger('ytb').setLevel(logging.DEBUG)
    logging.getLogger('rocketgram').setLevel(logging.DEBUG)
    logging.getLogger('rocketgram.raw.in').setLevel(logging.INFO)
    logging.getLogger('rocketgram.raw.out').setLevel(logging.INFO)

    logger = logging.getLogger('ytb.settings')

    logger.info('Starting bot''s template in %s...', mode)

    _loader = jinja2.PrefixLoader({k: j2tools.YamlLoader(v) for k, v in templates.items()})
    _jinja = jinja2.Environment(loader=_loader, trim_blocks=True, lstrip_blocks=True,
                                extensions=[jinja2.ext.LoopControlExtension])
    data.get_t = j2tools.t_factory(_jinja)

    bot = mybot.get_bot(os.environ['TOKEN'].strip())

    if mode == 'updates':
        rocketgram.UpdatesExecutor.run(bot, drop_updates=bool(int(os.environ.get('DROP_UPDATES', 0))))
    else:
        port = int(os.environ['PORT']) if mode == 'heroku' else int(os.environ.get('WEBHOOK_PORT', 8080))
        rocketgram.AioHttpExecutor.run(bot,
                                       os.environ['WEBHOOK_URL'].strip(),
                                       os.environ.get('WEBHOOK_PATH', '/').strip(),
                                       host='0.0.0.0', port=port,
                                       drop_updates=bool(int(os.environ.get('DROP_UPDATES', 0))),
                                       webhook_remove=not mode == 'heroku')

    logger.info('Bye!')


if __name__ == '__main__':
    main()
