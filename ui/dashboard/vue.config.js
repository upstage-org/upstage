module.exports = {
    publicPath: '/',
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = "UpStage";
                return args;
            })
    },
    pwa: {
        name: 'UpStage',
        themeColor: "#30ac45",
        msTileColor: "#ffffff",
    }
}
