const path = require('path');

module.exports = {
    entry: path.join(__dirname, "src", "index.tsx"),
    output: {
        filename: 'bundle.js',
    },
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.(tsx|ts)$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },

            // {
            //     test: /\.m?js$/,
            //     exclude: /(node_modules|bower_components)/,
            //     use: {
            //         loader: 'babel-loader',
            //         options: {
            //             presets: ['@babel/preset-env']
            //         }
            //     }
            // },
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
    }
};