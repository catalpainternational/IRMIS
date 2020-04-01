const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');

module.exports = {
    context: path.resolve(__dirname, './src'),
    entry: {
        estrada: ['whatwg-fetch', './estrada.js'],
        contracts: ['./contracts.js'],
    },
    output: {
        filename: '[name].js',
        library: 'roads',
        libraryTarget: 'window',
    },
    resolve: {
        extensions: ['.ts', '.js'],
    },
    module: {
        rules: [
            {
                test: /\.riot.html$/,
                exclude: /node_modules/,
                use: {
                    loader: '@riotjs/webpack-loader',
                    options: { type: 'es5' }
                }
            },
            {
                test: /\.(ts|js)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            [
                                "@babel/preset-env",
                                {
                                    "corejs": "3",
                                    "useBuiltIns": "usage"
                                }
                            ],
                            "@babel/preset-typescript"
                        ]
                    }
                }
            },
            {
                test: /\.scss$/,
                exclude: /node_modules/,
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
                exclude: /node_modules/,
                use: {
                    loader: 'svg-url-loader',
                    options: {
                        encoding: 'base64',
                    },
                },
            },
            {
                test: /\.(woff|woff2)$/,
                exclude: /node_modules/,
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
    optimization: {
        splitChunks: {
            chunks: 'all', // include all types of chunks
        }
    },
    plugins: [
        new CleanWebpackPlugin(),
    ],
};
