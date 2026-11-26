        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "同义标记合并",
  "module": "标记叫法规则",
  "caption": "标记叫法规则",
  "detail": "复核员把同一障碍的两种叫法合并为新叫法。入口与偏好卡登记时仍可使用旧称，台账与算分统一切换。",
  "path": "/tag_aliases",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "alias",
      "label": "旧称"
    },
    {
      "name": "canonical",
      "label": "新叫法"
    },
    {
      "name": "serial",
      "label": "规则序号"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "merge_tags",
      "label": "合并两个叫法",
      "path": "/tag_aliases/merge-tags",
      "fields": [
        {
          "name": "code",
          "label": "规则编号",
          "kind": "text",
          "initial": "AL-01"
        },
        {
          "name": "alias",
          "label": "旧称",
          "kind": "text",
          "initial": "碎石"
        },
        {
          "name": "canonical",
          "label": "新叫法",
          "kind": "text",
          "initial": "碎石路面"
        }
      ],
      "help": "合并后入口与偏好卡立即改用新叫法；受影响的旧匹配分作废，需重新计算后才能交线路单。",
      "roles": [
        "reviewer"
      ],
      "success": "已合并"
    }
  ]
};

        export const {title} = page;
        export const key = "tag_aliases";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
