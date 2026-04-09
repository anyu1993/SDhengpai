// netlify/functions/contact.js
// 表单提交 → 飞书群机器人 Webhook 通知

const fetch = require('node-fetch');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  // 解析 form-urlencoded 或 JSON
  let name, phone, company, message;
  const contentType = event.headers['content-type'] || '';

  if (contentType.includes('application/x-www-form-urlencoded')) {
    const params = new URLSearchParams(event.body);
    name = params.get('name');
    phone = params.get('phone');
    company = params.get('company') || '未填写';
    message = params.get('message') || '未填写';
  } else {
    try {
      const body = JSON.parse(event.body);
      name = body.name;
      phone = body.phone;
      company = body.company || '未填写';
      message = body.message || '未填写';
    } catch (e) {
      return { statusCode: 400, body: 'Invalid JSON' };
    }
  }

  if (!name || !phone) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: '姓名和电话为必填项' })
    };
  }

  // 电话脱敏
  const phoneMask = phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

  // 飞书卡片消息
  const feishuPayload = {
    msg_type: 'interactive',
    card: {
      header: {
        title: { tag: 'plain_text', content: '📋 新客户留言' },
        template: 'blue'
      },
      elements: [
        {
          tag: 'div',
          text: {
            tag: 'lark_md',
            content: `**姓名：** ${name}\n**电话：** ${phoneMask}\n**公司：** ${company}`
          }
        },
        { tag: 'hr' },
        {
          tag: 'div',
          text: { tag: 'lark_md', content: `**留言内容：**\n${message}` }
        },
        { tag: 'hr' },
        {
          tag: 'note',
          elements: [
            { tag: 'plain_text', content: `⏰ 提交时间：${now}` },
            { tag: 'plain_text', content: ` | 🔗 来源：官网表单` }
          ]
        }
      ]
    }
  };

  const webhookUrl = process.env.FEISHU_WEBHOOK_URL;
  if (!webhookUrl) {
    console.error('FEISHU_WEBHOOK_URL not set');
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Webhook 未配置' })
    };
  }

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feishuPayload)
    });

    if (!response.ok) {
      throw new Error(`Feishu API error: ${response.status}`);
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true, message: '提交成功！我们会尽快与您联系' })
    };
  } catch (err) {
    console.error('Failed to send Feishu notification:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: '通知发送失败，请稍后重试' })
    };
  }
};
