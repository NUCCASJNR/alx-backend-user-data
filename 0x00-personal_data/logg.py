#!/usr/bin/env python3

import logging
#
# logging.basicConfig(filename='app.log', filemode='w', format=f'%(name)s - %(levelname)s - %(message)s')
# logging.warning('This will get logged to a file')

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')
