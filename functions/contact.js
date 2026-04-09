export async function onRequestPost(context) {
  const { request, env } = context;
  
  try {
    const formData = await request.formData();
    const name = formData.get('name') || '';
    const phone = formData.get('phone') || '';
    const message = formData.get('message') || '';
    
    // Get Feishu webhook from environment variable or use default
    const webhookUrl = env.FEISHU_WEBHOOK_URL || 'https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID';
    
    // Build message for Feishu
    const feishuMessage = {
      msg_type: 'text',
      content: {
        text: `📩 **网站询价请求**\n\n👤 姓名: ${name}\n📞 电话: ${phone}\n💬 留言: ${message}\n\n⏰ 时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`
      }
    };
    
    // Send to Feishu
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feishuMessage)
    });
    
    if (response.ok) {
      return new Response(JSON.stringify({ success: true, message: '提交成功！我们会尽快联系您。' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } else {
      return new Response(JSON.stringify({ success: false, message: '提交失败，请稍后重试。' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } catch (error) {
    return new Response(JSON.stringify({ success: false, message: '提交失败：' + error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
