var webpack = require('webpack')
var ExtractTextPlugin = require("extract-text-webpack-plugin")

module.exports = {
  entry: {
    main: './app/static/js/entry.js'
  },
  output: {
    path: __dirname + '/app/static',
    filename: 'resource/javascripts/main.js'
  },
  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('css')
      },
      {
       test: /.scss$/,
       loader: ExtractTextPlugin.extract('style', 'css!sass')
      },
      {
       test: /.vue$/,
       loader: ExtractTextPlugin.extract('vue')
      },
      {
        test:/\.js$/,
        loader:"babel-loader",
        query: {
          presets: ['es2015']
        }
      },
      { test: /\.(woff2?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/, loader: 'file?name=/resource/images/[name].[hash].[ext]' },
      { test: /\.(png|jpg|gif|swf)$/, loader: 'file?name=/resource/images/[name].[hash].[ext]' },
    ]
  },
  plugins: [
    new ExtractTextPlugin("/resource/style/style.css"),

    // new webpack.ProvidePlugin({
    //   'window.Vue': 'vue',
    // }),
    // new webpack.optimize.CommonsChunkPlugin('vue', 'vue.js'),
    // new webpack.DefinePlugin({
    //   'process.env': {
    //     NODE_ENV: '"production"'
    //   }
    // }),
    // new webpack.optimize.UglifyJsPlugin({
    //   compress: {
    //     warnings: false
    //   }
    // })
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    })
  ],

  resolve: {
    extensions: ['', '.js', '.vue'],
    /**
     * Vue v2.x 之後 NPM Package 預設只會匯出 runtime-only 版本，若要使用 standalone 功能則需下列設定
     */
    alias: {
      vue: 'vue/dist/vue.js'
    }
  }
}
