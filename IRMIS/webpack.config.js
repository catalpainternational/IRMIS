const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');

module.exports = {
    'entry': path.resolve(__dirname, 'src', 'irmis.js'),
    'output': {
        'filename': 'irmis.js',
        'library': 'roads',
        'libraryTarget': 'window'
    },
    'module': {
        'rules': [
            {
                'test': /\.js$/,
                'exclude': [ /node_modules/ ],
                'use': {
                    'loader': 'babel-loader',
                    'options': {
                        'presets': [ 'env' ]
                    }
                }
            },
            {
                'test': /\.scss$/,
                'exclude': [ /node_modules/ ],
                'use': [
                    {
                        'loader': 'file-loader',
                        'options': {
                            'name': '[name].css'
                        }
                    },
                    { 'loader': 'extract-loader' },
                    { 'loader': 'css-loader' },
                    { 'loader': 'sass-loader' }
                ]
            }
        ]
    },
    'plugins': [
        new CleanWebpackPlugin()
    ]
};
