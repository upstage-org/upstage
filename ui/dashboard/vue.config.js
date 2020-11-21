module.exports = {
  transpileDependencies: ["vuetify"],
  publicPath: process.env.NODE_ENV === "development" ? "/" : "/V2.0/dashboard/",
  configureWebpack: {
    performance: {
      hints: false, // enum
      maxAssetSize: 1048576, // int (in bytes),
      maxEntrypointSize: 1048576, // int (in bytes)
    },
  },
};
