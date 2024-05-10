<script lang="tsx">
import { h } from "vue";
import { defineComponent, watch, reactive } from "vue";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Image from "@tiptap/extension-image";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";
import Toolbox from "./Toolbox.vue";
import { Space } from "ant-design-vue";

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const editor = useEditor({
      editorProps: {
        attributes: {
          class: "prose focus:outline-none",
        },
      },
      content: props.modelValue,
      onUpdate: ({ editor }) => {
        emit("update:modelValue", editor.getHTML());
      },
      editable: !props.readonly,
      extensions: [
        StarterKit,
        Link.configure({
          openOnClick: false,
          autolink: true,
        }),
        Image.configure({
          inline: true,
          allowBase64: true,
        }),
        Placeholder.configure({
          placeholder: props.placeholder,
        }),
      ],
    });

    watch(
      () => props.readonly,
      (newValues) => {
        editor?.value?.setEditable(!newValues)
      },
    );

    return () =>
      h(
        Space,
        {
          direction: "vertical",
          class: "w-full shadow rounded-xl bg-white p-4",
        },
        () => [
          !props.readonly && editor.value && h(Toolbox, { editor: editor.value }),
          h(EditorContent, {
            editor: editor.value,
          }),
        ],
      );
  }
});
</script>
