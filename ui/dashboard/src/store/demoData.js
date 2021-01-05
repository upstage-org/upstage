import config from "@/../vue.config";

export const generateDemoData = () => {

    const avatarFiles = [
        "01.png",
        "02.png",
        "03.png",
        "04.png",
        "05.png",
        "06.png",
        "07.png",
        "08.png",
        "09.png",
        "10.png",
        "11.png",
        "blob_avatar_1.jpg",
        "blob_avatar_2.jpg",
        "logo-upstage-official-print_500px.png",
        "mobilise-demoblise-logo-version-black.gif",
        "mobilise-demoblise-logo-version-white.png",
        "plague_doctor_clearcut2.png",
        "plague_doctor_clearcut.png",
        "virus_1.png",
        "virus_2.png",
        "virus_3.png",
    ];
    const avatars = avatarFiles.map((file) => ({
        name: file,
        src: `${config.publicPath}demo/avatars/${file}`,
    }));
    const backdrops = [
        {
            name: "1",
            src: config.publicPath + "demo/backdrops/1.jpg",
        },
        {
            name: "2",
            src: config.publicPath + "demo/backdrops/2.jpg",
        },
        {
            name: "3",
            src: config.publicPath + "demo/backdrops/3.jpg",
        },
        {
            name: "4",
            src: config.publicPath + "demo/backdrops/4.jpg",
        },
        {
            name: "5",
            src: config.publicPath + "demo/backdrops/5.jpg",
        },
        {
            name: "6",
            src: config.publicPath + "demo/backdrops/6.jpg",
        },
    ];


    const propFiles = ["facemask_filter.png", "quarantini_clearcut.png"];
    const props = propFiles.map((file) => ({
        name: file,
        src: `${config.publicPath}demo/props/${file}`,
    }));

    const audioFiles = ['applause.mp3', 'op11.mp3', 'typing.mp3', 'LDBoogie.mp3', 'sea_waves.mp3']
    const audios = audioFiles.map(file => {
        const name = file.split('.')[0].replace('_', ' ');
        const src = `${config.publicPath}demo/audios/${file}`;
        return { name, src, file };
    })

    const stageConfig = {
        animateDuration: 500,
    }

    return { avatars, props, backdrops, audios, config: stageConfig }
}
