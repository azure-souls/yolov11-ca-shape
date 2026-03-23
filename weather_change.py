import carla
import time

def main():
    # 1. 初始化客户端并连接CARLA，只加载一次地图
    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)
    
    # 检查是否已加载目标地图，未加载时才加载（避免重复加载）
    current_world_name = client.get_world().get_map().name
    target_world = 'Town10HD'
    if target_world not in current_world_name:
        print(f"首次加载地图: {target_world}")
        world = client.load_world(target_world)
    else:
        print(f"地图 {target_world} 已加载，直接复用")
        world = client.get_world()

    # 2. 初始天气参数（可作为默认值）
    current_weather = carla.WeatherParameters(
        precipitation_deposits=70,
        wind_intensity=50,
        sun_azimuth_angle=0,
        sun_altitude_angle=0.0,
        fog_distance=10,
        wetness=70,
        fog_falloff=0.1,
        cloudiness=70,
        precipitation=70.0,
        fog_density=15,
    )
    world.set_weather(current_weather)
    print("初始天气已设置完成！")
    print("可修改的参数：precipitation_deposits(积雨)、wind_intensity(风速)、sun_azimuth_angle(太阳方位角)、sun_altitude_angle(太阳高度角)")
    print("输入格式示例：precipitation_deposits=80 或直接按回车保持当前值，输入q退出\n")

    # 3. 交互式修改天气（不重新加载地图）
    while True:
        # 逐个参数询问修改
        print(f"\n当前参数：")
        print(f"积雨(0-100)：{current_weather.precipitation_deposits}")
        print(f"风速(0-100)：{current_weather.wind_intensity}")
        print(f"太阳方位角(0-360)：{current_weather.sun_azimuth_angle}")
        print(f"太阳高度角(-90-90)：{current_weather.sun_altitude_angle}")

        # 读取用户输入
        user_input = input("\n请输入要修改的参数（如：wind_intensity=20）：").strip()
        
        # 退出条件
        if user_input.lower() == 'q':
            break
        
        # 解析输入并修改参数
        if '=' in user_input:
            try:
                param, value = user_input.split('=')
                param = param.strip()
                value = float(value.strip())

                # 更新对应参数
                if hasattr(current_weather, param):
                    # 创建新的天气对象（carla.WeatherParameters是不可变对象，需重新创建）
                    weather_kwargs = {
                        'precipitation_deposits': current_weather.precipitation_deposits,
                        'wind_intensity': current_weather.wind_intensity,
                        'sun_azimuth_angle': current_weather.sun_azimuth_angle,
                        'sun_altitude_angle': current_weather.sun_altitude_angle,
                        'fog_distance': current_weather.fog_distance,
                        'wetness': current_weather.wetness,
                        'fog_falloff': current_weather.fog_falloff,
                        'cloudiness': current_weather.cloudiness,
                        'precipitation': current_weather.precipitation,
                        'fog_density': current_weather.fog_density,
                    }
                    weather_kwargs[param] = value
                    current_weather = carla.WeatherParameters(**weather_kwargs)
                    
                    # 应用新天气（核心：只改天气，不改地图）
                    world.set_weather(current_weather)
                    print(f"✅ 已更新 {param} = {value}，天气已生效！")
                else:
                    print(f"❌ 无效参数：{param}，请检查参数名")
            except ValueError:
                print("❌ 输入格式错误，请输入 参数名=数值（如：sun_altitude_angle=60）")
        elif user_input == '':
            continue  # 按回车跳过，保持当前参数
        else:
            print("❌ 输入格式错误，请输入 参数名=数值 或 q退出")
        
        # 给一点时间让天气效果加载
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户手动中断程序")
    finally:
        print('结束仿真')