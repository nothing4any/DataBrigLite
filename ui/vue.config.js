const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  publicPath: '/ui/',
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '': {
        target: 'http://127.0.0.1:5001',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          // '^/': '',
        },
      },
    },
  },
  });
