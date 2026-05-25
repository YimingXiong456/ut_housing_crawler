from playwright.sync_api import sync_playwright
import time
import random
import winsound
import threading

def play_loud_alarm():
    """疯狂警报声（立即播放）"""
    print("\n" + "!"*80)
    print("🚨 🚨 🚨  UT HOUSING 发现房源！！！快去选房！！！ 🚨 🚨 🚨")
    print("!"*80)
    
    while True:
        winsound.Beep(1800, 350)
        time.sleep(0.15)
        winsound.Beep(2300, 250)
        time.sleep(0.1)
        winsound.Beep(1500, 400)
        time.sleep(0.2)

def is_logged_in(page):
    try:
        return page.locator('a:has-text("application status")').count() > 0
    except:
        return False

def has_rooms_available(page):
    try:
        body_text = page.text_content('body').lower()
        if "couldn't find any rooms" in body_text:
            return False
        if page.locator('button:has-text("SELECT ROOM"), div[class*="room-tile"]').count() > 0:
            return True
        return False
    except:
        return False

def attempt_select_room(page, is_first_attempt):
    try:
        print("   → 点击 Application Status")
        page.locator('a:has-text("application status")').click()
        
        page.wait_for_url("**Housing_Application**", timeout=25000)
        time.sleep(2)
        
        print("   → 点击 CONTINUE")
        page.locator('button:has-text("CONTINUE")').click()
        
        page.wait_for_url("**Select_Your_Room**", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(4)
        
        if is_first_attempt:
            # 第一次：只勾选 45%
            print("   → 第一次：勾选 2 Bedroom (45%)")
            page.locator('label:has-text("2 Bedroom (45%)")').click()
            time.sleep(3)
        else:
            # 后续轮次：只用 55% 点击两次刷新过滤器，**绝不碰45%**
            print("   → 后续：用 2 Bedroom (55%) 刷新过滤器")
            label_55 = page.locator('label:has-text("2 Bedroom (55%)")')
            label_55.click()
            time.sleep(1.5)
            label_55.click()   # 第二次点击取消
            time.sleep(3)
        
        # 判断是否有房源
        if has_rooms_available(page):
            print("🎉 🎉 检测到房源！")
            page.screenshot(path=f"room_available_{time.strftime('%H%M%S')}.png")
            return True
        else:
            print("❌ 当前暂无房源，继续监控...")
            return False
            
    except Exception as e:
        print(f"⚠️ 流程出错: {e}")
        page.screenshot(path=f"error_{time.strftime('%H%M%S')}.png")
        return False


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        attempt_count = 0
        
        while True:
            attempt_count += 1
            is_first = (attempt_count == 1)
            print(f"\n🔄 第 {attempt_count} 次尝试... ({time.strftime('%H:%M:%S')})")
            
            try:
                page.goto("https://utaustin.starrezhousing.com/StarRezPortalX", wait_until="domcontentloaded", timeout=30000)
                
                if not is_logged_in(page):
                    print("   → 需要登录")
                    page.locator('a[href*="InitiateLogin"]').click()
                    page.wait_for_url("**enterprise.login.utexas.edu**", timeout=25000)
                    time.sleep(2)
                    page.fill('input#username', 'xxxx')
                    page.fill('input#password', 'xxxx')
                    page.locator('input[type="submit"], input[value*="Sign"]').click()
                    page.wait_for_url("**StarRezPortalX**", timeout=40000)
                    time.sleep(3)
                else:
                    print("   → 已登录")
                
                has_room = attempt_select_room(page, is_first)
                
                if has_room:
                    alarm_thread = threading.Thread(target=play_loud_alarm, daemon=True)
                    alarm_thread.start()
                    print("\n🎯 警报已启动！蜂鸣声正在疯狂播放！")
                    input("\n按回车键停止警报并关闭浏览器...")
                    break
                    
            except Exception as e:
                print(f"❌ 本轮出错: {e}")
            
            wait_time = 180 + random.randint(-2, 3)
            print(f"⏳ 下次尝试将在 {wait_time} 秒后进行...")
            time.sleep(wait_time)


if __name__ == "__main__":
    main()