import { URL } from 'whatwg-url';
import { Buffer } from 'buffer/';

global.URL = URL;
global.Buffer = Buffer;

import('./src');
