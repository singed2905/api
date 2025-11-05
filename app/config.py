"""
Application configuration settings

Implementation hoàn chỉnh của Pydantic BaseSettings để load
configuration từ environment variables và JSON files.

Features:
- Load từ .env file và environment variables
- Dynamic loading các JSON configs
- Support cho tất cả calculator versions
- Geometry operations và encoding rules
"""

from pydantic_settings import BaseSettings
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Main settings class cho Geometry Calculator API
    
    Tự động load từ:
    - Environment variables
    - .env file 
    - JSON configuration files
    """
    
    # =================================================================
    # API SETTINGS
    # =================================================================
    app_name: str = "Geometry Calculator API"
    app_version: str = "2.1.0"
    debug: bool = True
    
    # =================================================================
    # SERVER SETTINGS  
    # =================================================================
    host: str = "0.0.0.0"
    port: int = 8000
    
    # =================================================================
    # FILE PROCESSING SETTINGS
    # =================================================================
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    upload_dir: str = "uploads"
    output_dir: str = "outputs"
    large_file_threshold: int = 50 * 1024 * 1024  # 50MB
    
    # =================================================================
    # SECURITY SETTINGS
    # =================================================================
    allowed_origins: List[str] = ["*"]
    allowed_file_types: List[str] = [".xlsx", ".xls"]
    
    # =================================================================
    # PROCESSING SETTINGS
    # =================================================================
    chunk_size: int = 1000
    max_background_tasks: int = 5
    cleanup_interval_hours: int = 24
    processing_timeout: int = 300
    
    # =================================================================
    # GEOMETRY SERVICE SETTINGS
    # =================================================================
    default_calculator_version: str = "fx799"
    supported_versions: List[str] = ["fx799", "fx880", "fx991", "fx570", "fx801"]
    
    # =================================================================
    # CONFIG PATHS
    # =================================================================
    config_dir: str = "config"
    geometry_config_path: str = "config/geometry_mode"
    version_configs_path: str = "config/version_configs"
    common_config_path: str = "config/common"
    
    # =================================================================
    # DATABASE (Optional)
    # =================================================================
    database_url: str = "sqlite:///./geometry_api.db"
    
    # =================================================================
    # LOGGING SETTINGS
    # =================================================================
    log_level: str = "INFO"
    log_file: str = "logs/geometry_api.log"
    
    def load_json_config(self, file_path: str) -> Dict[str, Any]:
        """
        Load JSON configuration file safely
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dictionary with config data, empty dict if file not found
        """
        try:
            if not os.path.exists(file_path):
                return {}
                
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {file_path}: {e}")
            return {}
        except Exception as e:
            print(f"Warning: Error loading {file_path}: {e}")
            return {}
    
    @property
    def modes_config(self) -> Dict[str, Any]:
        """Get main modes configuration"""
        path = os.path.join(self.config_dir, "modes.json")
        return self.load_json_config(path)
    
    @property
    def geometry_operations(self) -> Dict[str, Any]:
        """Get geometry operations configuration"""
        path = os.path.join(self.geometry_config_path, "geometry_operations.json")
        return self.load_json_config(path)
    
    @property
    def geometry_excel_mapping(self) -> Dict[str, Any]:
        """Get Excel mapping configuration for geometry"""
        path = os.path.join(self.geometry_config_path, "geometry_excel_mapping.json")
        return self.load_json_config(path)
    
    @property
    def encoding_rules(self) -> Dict[str, Any]:
        """Get LaTeX to calculator encoding rules"""
        path = os.path.join(self.geometry_config_path, "encoding_rules.json")
        return self.load_json_config(path)
    
    @property
    def keylog_patterns(self) -> Dict[str, Any]:
        """Get keylog encoding patterns"""
        path = os.path.join(self.geometry_config_path, "keylog_patterns.json")
        return self.load_json_config(path)
    
    @property
    def versions_config(self) -> Dict[str, Any]:
        """Get supported versions configuration"""
        path = os.path.join(self.common_config_path, "versions.json")
        return self.load_json_config(path)
    
    @property
    def version_mapping(self) -> Dict[str, Any]:
        """Get version to config file mapping"""
        path = os.path.join(self.common_config_path, "version_mapping.json")
        return self.load_json_config(path)
    
    @property
    def calculator_configs(self) -> Dict[str, Any]:
        """
        Get all calculator version configurations
        
        Returns:
            Dict with version as key and config as value
        """
        configs = {}
        config_dir = Path(self.version_configs_path)
        
        if not config_dir.exists():
            return configs
            
        for json_file in config_dir.glob("*.json"):
            try:
                # Extract version from filename
                filename = json_file.stem
                if '_config' in filename:
                    version = filename.replace('_config', '')
                elif 'fx' in filename:
                    # Handle files like fx991_fx570_config.json
                    if '_' in filename and 'fx' in filename:
                        # Load multi-version file
                        multi_config = self.load_json_config(str(json_file))
                        configs.update(multi_config)
                        continue
                    else:
                        version = filename
                else:
                    version = filename
                    
                config_data = self.load_json_config(str(json_file))
                if config_data:
                    configs[version] = config_data
                    
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")
                continue
                
        return configs
    
    def get_calculator_config(self, version: str) -> Dict[str, Any]:
        """
        Get specific calculator configuration
        
        Args:
            version: Calculator version (fx799, fx880, etc.)
            
        Returns:
            Configuration dict for the calculator version
        """
        all_configs = self.calculator_configs
        return all_configs.get(version, {})
    
    def get_supported_operations(self) -> List[str]:
        """Get list of supported geometry operations"""
        ops = self.geometry_operations
        return list(ops.get("operations", {}).keys())
    
    def get_supported_shapes(self) -> List[str]:
        """Get list of all supported shapes"""
        ops = self.geometry_operations
        shapes = set()
        
        # From coordinate systems
        coord_systems = ops.get("coordinate_systems", {})
        for dim_info in coord_systems.values():
            shapes.update(dim_info.get("supported_objects", []))
        
        return list(shapes)
    
    def validate_operation_combination(self, operation: str, shape_a: str, shape_b: str = None) -> bool:
        """
        Validate if an operation combination is supported
        
        Args:
            operation: Operation type
            shape_a: First shape
            shape_b: Second shape (optional)
            
        Returns:
            True if combination is valid
        """
        ops = self.geometry_operations
        operations = ops.get("operations", {})
        
        if operation not in operations:
            return False
            
        op_config = operations[operation]
        
        # Check single-shape operations (like Area, Volume)
        if "supported_objects" in op_config:
            supported = [obj["type"] for obj in op_config["supported_objects"]]
            return shape_a in supported
        
        # Check two-shape operations (like Distance, Intersection)
        if "supported_combinations" in op_config and shape_b:
            combinations = op_config["supported_combinations"]
            for combo in combinations:
                if (combo["type1"] == shape_a and combo["type2"] == shape_b) or \
                   (combo["type1"] == shape_b and combo["type2"] == shape_a):
                    return True
        
        return False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

# Global settings instance
settings = Settings()
