const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');

module.exports = {
    context: path.resolve(__dirname, './src'),
    entry: {
        app: './irmis.ts',
    },
    output: {
        filename: 'irmis.js',
        library: 'roads',
        libraryTarget: 'window',
    },
    resolve: {
        extensions: ['.ts', '.js'],
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: [/node_modules/],
                use: [
                    { loader: 'ts-loader' },
                ],
            },
            {
                test: /\.scss$/,
                exclude: [/node_modules/],
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].css',
                        },
                    },
                    { loader: 'extract-loader' },
                    { loader: 'css-loader' },
                    { loader: 'sass-loader' },
                ],
            },
            {
                test: /\.svg$/,
                exclude: [/node_modules/],
                use: {
                    loader: 'svg-url-loader',
                    options: {
                        encoding: 'base64',
                    },
                },
            },
            {
                test: /\.(woff|woff2)$/,
                exclude: [/node_modules/],
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                    },
                },
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: {
                    loader: 'url-loader',
                },
            },
        ],
    },
    plugins: [
        new CleanWebpackPlugin(),
    ],
};
