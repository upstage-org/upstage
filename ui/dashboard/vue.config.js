module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
        ? '/V4.0/ui/'
        : '/',
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = "UpStage";
                return args;
            })
    }
}
