const path = require('path');

module.exports = {
    watch: true,
    mode: 'development',
    entry: {
        base: './static/js/base.js',//ベース
        recipes: './static/js/recipes.js',
        recipe_create: './static/js/recipe_create.js',
        recipe_detail:'./static/js/recipe_detail.js',
        mypage:'./static/js/mypage.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, './recipe/static/recipe/js')
    },
    //ソースマップの設定（どこでエラーしたかがわかるようになる）
    devtool: 'cheap-module-eval-source-map',

    module: {
        rules: [
            {
                test: /\.scss$/,
                //ローダーの処理対象となるディレクトリ
                include: path.resolve(__dirname, './static/scss/'),
                use: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            },
            // ファイルをローディングする場合の設定
            {
                test: /\.(png|jpg|jpeg|gif)$/i,
                include: path.resolve(__dirname, './static/img/'),
                loader: 'url-loader',
                options: {
                    limit: 8192,
                    name: '[name].[ext]',
                    outputs: '../img/',
                    publicPath: path => './img/' + path,
                }
            }
        ],
    }
}