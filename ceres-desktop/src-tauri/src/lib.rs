use tauri_plugin_shell::ShellExt;
use tauri::Manager;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let shell = app.shell();
            
            // Try production path first (bundled resources)
            if let Ok(resource_dir) = app.path().resource_dir() {
                let script_path = resource_dir.join("start.sh");
                
                if script_path.exists() {
                    println!("📦 Using bundled script at: {:?}", script_path);
                    let command = shell.command("/bin/bash").args([script_path.to_str().unwrap()]);
                    
                    match command.spawn() {
                        Ok((_rx, child)) => {
                            println!("✅ Backend script started (PID: {})", child.pid());
                            return Ok(());
                        }
                        Err(e) => {
                            eprintln!("❌ Failed to start bundled script. Error: {:?}", e);
                        }
                    }
                }
            }
            
            // Fallback to development path
            let dev_script_path = "/Users/piyush/Desktop/ceres/src-tauri/start.sh";
            println!("🔧 Falling back to development script at: {}", dev_script_path);
            
            let command = shell.command("/bin/bash").args([dev_script_path]);
            
            match command.spawn() {
                Ok((_rx, child)) => {
                    println!("✅ Backend script started (PID: {})", child.pid());
                }
                Err(e) => {
                    eprintln!("❌ Failed to start development script. Error: {:?}", e);
                    eprintln!("Make sure the script exists and is executable:");
                    eprintln!("  chmod +x {}", dev_script_path);
                }
            }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("❌ Error running Tauri app");
}