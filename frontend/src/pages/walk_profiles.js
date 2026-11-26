        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const rankedView = result => el('div', {class:'scroll'},
          el('table', {},
            el('thead', {}, el('tr', {}, ['候选入口','匹配分','坡道通行','扣分项'].map(h => el('th',{scope:'col'},h)))),
            el('tbody', {}, (result.ranked || []).map(item =>
              el('tr', {},
                el('td', {}, item.entry),
                el('td', {}, String(item.score)),
                el('td', {}, item.ramp ? '是' : '否'),
                el('td', {}, (item.deductions || []).length
                  ? item.deductions.map(d => d.item + ' 扣 ' + d.weight).join('；')
                  : '无扣分'))))));

        const page = {
  "title": "无障碍障碍组合",
  "module": "绕行偏好卡",
  "caption": "绕行偏好卡",
  "detail": "声明应避开的设施标记与优先级。同义叫法合并后按新叫法计分，同一障碍只扣一次，重复项取较重权重。",
  "path": "/walk_profiles",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "park",
      "label": "公园"
    },
    {
      "name": "avoid",
      "label": "需避开标记"
    },
    {
      "name": "weights",
      "label": "标记权重"
    },
    {
      "name": "minimum",
      "label": "最低匹配分"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "draft_profile",
      "label": "记录绕行条件",
      "path": "/walk_profiles/draft-profile",
      "fields": [
        {
          "name": "code",
          "label": "偏好卡号",
          "kind": "text",
          "initial": "PR-11"
        },
        {
          "name": "park",
          "label": "公园",
          "kind": "text",
          "initial": "柳瓦园"
        },
        {
          "name": "avoid",
          "label": "应规避标记",
          "kind": "json",
          "initial": [
            "石阶",
            "碎石"
          ]
        },
        {
          "name": "weights",
          "label": "阻碍权重",
          "kind": "json",
          "initial": {
            "石阶": 2,
            "碎石": 1
          }
        },
        {
          "name": "minimum",
          "label": "最低匹配分",
          "kind": "float",
          "initial": 0.7
        }
      ],
      "help": "避开标记与权重键一一对应。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "match_entrances",
      "label": "计算地图候选入口",
      "path": "/walk_profiles/match-entrances",
      "fields": [
        {
          "name": "profile",
          "label": "偏好卡号",
          "kind": "text",
          "initial": "PR-11"
        }
      ],
      "help": "按障碍权重从高到低列出候选入口，并列出新分扣了哪几项。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入",
      "present": rankedView
    }
  ]
};

        export const {title} = page;
        export const key = "walk_profiles";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
