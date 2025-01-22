import os
import subprocess
import shutil

def create_rust_project_with_icon():
    print("=== Rust Project Creator with Icon Embedding ===")
    
    # Get user input
    project_name = input("Enter the name of your Rust project: ").strip()
    icon_path = input("Enter the full path to your .ico file: ").strip()
    
    # Validate .ico file path
    if not os.path.isfile(icon_path) or not icon_path.lower().endswith('.ico'):
        print("Error: Invalid .ico file path.")
        return

    # Create the Rust project
    print(f"Creating Rust project '{project_name}'...")
    subprocess.run(["cargo", "new", "--bin", project_name], check=True)
    
    project_dir = os.path.join(os.getcwd(), project_name)
    os.chdir(project_dir)
    
    # Create .rc file
    rc_file_content = f'app_icon ICON "{os.path.basename(icon_path)}"'
    rc_file_path = os.path.join(project_dir, "app_icon.rc")
    with open(rc_file_path, "w") as rc_file:
        rc_file.write(rc_file_content)

    # Copy the .ico file into the project directory
    shutil.copy(icon_path, project_dir)

    # Create build.rs
    build_rs_content = """\
fn main() {
    #[cfg(windows)]
    {
        embed_resource::compile("app_icon.rc", std::iter::empty::<&str>());
    }
}
"""
    with open(os.path.join(project_dir, "build.rs"), "w") as build_rs:
        build_rs.write(build_rs_content)

    # Update Cargo.toml
    cargo_toml_path = os.path.join(project_dir, "Cargo.toml")
    with open(cargo_toml_path, "a") as cargo_toml:
        cargo_toml.write('\n[build-dependencies]\nembed-resource = "2.5"\n')
        cargo_toml.write('\n[package.metadata.winres]\nres = "app_icon.res"\n')

    # Display completion message
    print(f"Project '{project_name}' created successfully with icon support!")
    print(f"To build your project, navigate to {project_dir} and run: cargo build --release")

if __name__ == "__main__":
    create_rust_project_with_icon()
