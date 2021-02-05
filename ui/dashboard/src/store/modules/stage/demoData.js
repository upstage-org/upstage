import config from "@/../vue.config";

export const generateDemoData = () => {

    const avatars = [
        {
            name: "Helen",
            src: "01.png",
            multi: true,
            frames: [
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
            ]
        },
        {
            name: 'Julius',
            src: "julius_01.png",
            multi: true,
            frames: [
                "julius_01.png",
                "julius_03.png",
                "julius_05.png",
                "julius_07.png",
                "julius_08.png",
                "julius_10.png",
            ]
        },
        {
            name: 'Blob',
            src: "blob_avatar_1.png",
            multi: true,
            frames: [
                "blob_avatar_1.png",
                "blob_avatar_2.png",
            ]
        },
        {
            name: 'Dave',
            src: "dave_02.png",
            multi: true,
            frames: [
                "dave_02.png",
                "dave_05.png",
                "dave_07.png",
                "dave_11.png",
                "dave_14.png",
                "dave_15.png",
            ]
        },
        {
            name: 'Manunui',
            src: "Manunui1.png",
            multi: true,
            frames: [
                "Manunui1.png",
                "Manunui2.png",
                "Manunui3.png",
                "Manunui4.png",
                "Manunui5.png",
            ]
        },
        {
            name: 'ViAv',
            src: "ViAv1.png",
            multi: true,
            frames: [
                "ViAv1.png",
                "ViAv2.png",
                "ViAv3.png",
                "ViAv4.png",
                "ViAv5.png",
            ]
        },
        {
            name: 'VincentPalace',
            src: "VincentPalace.png",
        },
        {
            name: 'VicPalace',
            src: "VicPalace.png",
        },
        {
            name: 'AudreyAv',
            src: "AudreyAv.png",
        },
        {
            name: 'lololol',
            src: "lololol.png",
        },
        {
            name: 'Pan',
            src: "Pan.png",
        },
        {
            name: 'Icarus',
            src: "Icarus.png",
        },

    ]
    avatars.forEach(avatar => {
        avatar.src = `${config.publicPath}demo/avatars/${avatar.src}`
        avatar.frames = avatar.frames?.map(frame => `${config.publicPath}demo/avatars/${frame}`)
    })

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
        {
            name: "map",
            src: config.publicPath + "demo/backdrops/map.png",
        },
        {
            name: "monarch_butterfly_backdrop",
            src: config.publicPath + "demo/backdrops/monarch_butterfly_backdrop.jpg",
        },
        {
            name: "tunnel_beach",
            src: config.publicPath + "demo/backdrops/tunnel_beach_02.jpg",
        },
        {
            name: "Chart",
            src: config.publicPath + "demo/backdrops/Chart.jpg",
        },
        {
            name: 'Refinery',
            src: config.publicPath + "demo/backdrops/Refinery.png",
        }
    ];


    const propFiles = ["quarantini_clearcut.png", "logo-upstage-official-print_500px.png", "mobilise-demoblise-logo-version-black.gif", "mobilise-demoblise-logo-version-white.png", "DrGraham.png", "Linsky.png", "Nelson.png", "hamilton.png", "romney.png", "campbellStokes.png"];
    const props = propFiles.map((file) => ({
        name: file.split('.')[0].replace(/_/g, ' '),
        src: file,
    })).concat([{
        name: 'Brolly',
        src: "brolly.png",
        multi: true,
        frames: ["brolly.png", "brolly1.png"]
    }]).concat([{
        name: 'Spiraldance',
        src: "spiraldance.png",
        multi: true,
        frames: ["spiraldance.png", "spiraldance1.png"]
    }]);

    props.forEach(prop => {
        prop.src = `${config.publicPath}demo/props/${prop.src}`
        prop.frames = prop.frames?.map(frame => `${config.publicPath}demo/props/${frame}`)
        prop.type = 'prop';
    })

    const audioFiles = ['applause.mp3', 'op11.mp3', 'typing.mp3', 'LDBoogie.mp3', 'sea_waves.mp3', 'rain_thunder_5m.mp3', 'thunder.mp3']
    const audios = audioFiles.map(file => {
        const name = file.split('.')[0].replace(/_/g, ' ');
        const src = `${config.publicPath}demo/audios/${file}`;
        return { name, src, file };
    })

    const streams = [{ type: "stream", url: `${config.publicPath}demo/streams/bunny.mp4`, metadata: { _vei: {}, _vod: "" }, w: 320, h: 176 }];

    const stageConfig = {
        width: 1280,
        height: 800,
        animateDuration: 500,
    }

    return { avatars, props, backdrops, audios, streams, config: stageConfig }
}
