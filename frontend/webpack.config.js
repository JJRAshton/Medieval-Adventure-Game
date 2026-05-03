const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: path.join(__dirname, "src", "index.tsx"),
    output: {
        filename: 'bundle.js',
    },
    mode: 'development',
    devServer: {
        hot: false,
    },
    module: {
        rules: [
            {
                test: /\.tsx$/i,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"],
            },
            {
                test: /\.png$/i,
                use: [
                  {
                    loader: 'file-loader',
                  },
                ],
              },
        ],
    },
    resolve: {
        extensions: ['', '.png', '.tsx'],
    },
    plugins: [
        new HtmlWebpackPlugin({ template: path.join(__dirname, 'src', 'index.html') }),
    ],
};