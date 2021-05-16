export function getStageMedia(stage) {
    let value = stage.attributes.find(a => a.name === 'media')?.description;
    if (value) {
        return JSON.parse(value);
    } else {
        return []
    }
}