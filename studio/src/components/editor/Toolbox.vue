<script lang="tsx">
import { defineComponent } from "vue";
import { PropType } from "vue";
import { Editor } from "@tiptap/vue-3";
import { Button, ButtonGroup, Modal, Space, message } from "ant-design-vue";
import { h } from "vue";
import {
  BoldOutlined,
  ItalicOutlined,
  ClearOutlined,
  LinkOutlined,
  CodeOutlined,
  OrderedListOutlined,
  UnorderedListOutlined,
  StrikethroughOutlined,
  CommentOutlined,
  LineOutlined,
  EnterOutlined,
  PictureOutlined,
} from "@ant-design/icons-vue";
import { VNode } from "vue";
import { ref } from "vue";

export interface ToolbarItem {
  type: string;
  icon: VNode;
  disabled?: boolean;
  action: () => void;
  isActive?: () => boolean;
}

export default defineComponent({
  props: {
    editor: { type: Object as PropType<Editor>, required: true },
  },
  setup(props) {
    const showInstruction = ref(false);
    const toolbars: ToolbarItem[][] = [
      [
        {
          type: "heading1",
          icon: h("span", "H1"),
          action: () =>
            props.editor.chain().focus().toggleHeading({ level: 1 }).run(),
          isActive: () => props.editor.isActive("heading", { level: 1 }),
        },
        {
          type: "heading2",
          icon: h("span", "H2"),
          action: () =>
            props.editor.chain().focus().toggleHeading({ level: 2 }).run(),
          isActive: () => props.editor.isActive("heading", { level: 2 }),
        },
        {
          type: "heading3",
          icon: h("span", "H3"),
          action: () =>
            props.editor.chain().focus().toggleHeading({ level: 3 }).run(),
          isActive: () => props.editor.isActive("heading", { level: 3 }),
        },
      ],
      [
        {
          type: "bulletList",
          icon: h(UnorderedListOutlined),
          action: () => props.editor.chain().focus().toggleBulletList().run(),
          isActive: () => props.editor.isActive("bulletList"),
        },
        {
          type: "orderedList",
          icon: h(OrderedListOutlined),
          action: () => props.editor.chain().focus().toggleOrderedList().run(),
          isActive: () => props.editor.isActive("orderedList"),
        },
      ],
      [
        {
          type: "bold",
          icon: h(BoldOutlined),
          disabled: !props.editor.can().chain().focus().toggleBold().run(),
          action: () => props.editor.chain().focus().toggleBold().run(),
          isActive: () => props.editor.isActive("bold"),
        },
        {
          type: "italic",
          icon: h(ItalicOutlined),
          disabled: !props.editor.can().chain().focus().toggleItalic().run(),
          action: () => props.editor.chain().focus().toggleItalic().run(),
          isActive: () => props.editor.isActive("italic"),
        },
        {
          type: "strike",
          icon: h(StrikethroughOutlined),
          disabled: !props.editor.can().chain().focus().toggleStrike().run(),
          action: () => props.editor.chain().focus().toggleStrike().run(),
          isActive: () => props.editor.isActive("strike"),
        },
        {
          type: "clear",
          icon: h(ClearOutlined),
          disabled: !props.editor.can().chain().focus().unsetAllMarks().run(),
          action: () => props.editor.chain().focus().unsetAllMarks().run(),
        },
        {
          type: "link",
          icon: h(LinkOutlined),
          disabled: !props.editor
            .can()
            .chain()
            .focus()
            .extendMarkRange("link")
            .unsetLink()
            .run(),
          action: () => (showInstruction.value = true),
          isActive: () => props.editor.isActive("link"),
        },
      ],
      [
        {
          type: "codeblock",
          icon: h(CodeOutlined),
          action: () => props.editor.chain().focus().toggleCodeBlock().run(),
          isActive: () => props.editor.isActive("codeBlock"),
        },
        {
          type: "blockquote",
          icon: h(CommentOutlined),
          action: () => props.editor.chain().focus().toggleBlockquote().run(),
          isActive: () => props.editor.isActive("blockquote"),
        },
        {
          type: "horizontalRule",
          icon: h(LineOutlined),
          action: () => props.editor.chain().focus().setHorizontalRule().run(),
        },
        {
          type: "hardBreak",
          icon: h(EnterOutlined),
          action: () => props.editor.chain().focus().setHardBreak().run(),
        },
        {
          type: "image",
          disabled: typeof props.editor.can().setImage === "undefined",
          icon: h(PictureOutlined),
          action: () => (showInstruction.value = true),
        },
      ],
    ];

    return () => [
      h(Space, () =>
        toolbars.map((toolbar, index) =>
          h(ButtonGroup, { key: index }, () =>
            toolbar
              .filter((item) => !item.disabled)
              .map((item) =>
                h(
                  Button,
                  {
                    key: item.type,
                    onClick: item.action,
                    size: "small",
                    type: item.isActive?.() ? "primary" : "default",
                  },
                  () => item.icon,
                ),
              ),
          ),
        ),
      ),
      h(
        Modal,
        {
          title: "Tips 💡",
          visible: showInstruction.value,
          "onUpdate:visible": () => (showInstruction.value = false),
          footer: null,
        },
        () =>
          h(Space, { direction: "vertical" }, () => [
            h("div", { class: "whitespace-pre" }, [
              h(LinkOutlined),
              ` To insert a link, follow these steps:\n1. Copy the URL of the link to the clipboard.\n2. Select the text that will contain the link.\n3. Press Ctrl+V to embed the link into the text.`,
            ]),
            h("div", { class: "whitespace-pre" }, [
              h(PictureOutlined),
              ` To insert an image, follow these steps:\n1. Copy the content of the image (not the link of it) to the clipboard.\n2. Press Ctrl+V to embed the image at the cursor caret.`,
            ]),
          ]),
      ),
    ];
  },
});
</script>
