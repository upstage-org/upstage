import configs from "@/config";
import { onMounted, ref } from "vue";
import { useStore } from "vuex";

export const useLowLevelAPI = () => {
  const { JitsiMeetJS } = window;
  return JitsiMeetJS;
}

export const useJitsiDomain = () => {
  const domain = configs.JITSI_ENDPOINT.replace(/(^https?:\/\/|\/)/g, "");
  return domain;
}

export const useJitsi = () => {
  const joined = ref(false);
  const jitsi = { room: null, connection: null };
  const domain = useJitsiDomain();
  const store = useStore();
  const stageUrl = store.getters['stage/url']

  const JitsiMeetJS = useLowLevelAPI();

  onMounted(() => {
    JitsiMeetJS.init();
    JitsiMeetJS.setLogLevel(JitsiMeetJS.logLevels.ERROR);
    jitsi.connection = new JitsiMeetJS.JitsiConnection(null, null, {
      hosts: {
        domain: domain,
        muc: `conference.${domain}`,
        focus: `focus.${domain}`
      },
      bosh: `https://${domain}/http-bind`,
    });

    jitsi.connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_ESTABLISHED, (e) => {
      console.log('Connection established', e);
      jitsi.room = jitsi.connection.initJitsiConference(stageUrl, {});
      jitsi.room.on(JitsiMeetJS.events.conference.TRACK_ADDED, (track) => {
        store.dispatch('stage/addTrack', track);
      });
      jitsi.room.on(JitsiMeetJS.events.conference.CONFERENCE_JOINED, (e) => {
        console.log('Conference joined', e);
        joined.value = true;
      });

      jitsi.room.join();
    });
    jitsi.connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_FAILED, (e) => {
      console.error('Connection failed', e);
      joined.value = false;
    });
    jitsi.connection.addEventListener(JitsiMeetJS.events.connection.CONNECTION_DISCONNECTED, (e) => {
      console.error('Connection disconnected', e);
      joined.value = false;
    });

    jitsi.connection.connect();
  })

  return [jitsi, joined];
}