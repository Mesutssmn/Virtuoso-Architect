"""
Central Configuration for Label Definitions
Supports both 4-label and 5-label configurations
"""

# Label configurations
LABEL_CONFIGS = {
    "4_labels": {
        0: "Far Reach",
        1: "Double Thirds",
        2: "Advanced Chords",
        3: "Advanced Counterpoint"
    },
    "5_labels": {
        0: "Far Reach",
        1: "Double Thirds",
        2: "Advanced Chords",
        3: "Advanced Counterpoint",
        4: "Multiple Voices"
    }
}

# Feature thresholds for auto-labeling
AUTO_LABEL_THRESHOLDS = {
    "4_labels": {
        "far_reach": {
            "max_stretch": 25,
            "octave_jump_frequency": 0.15
        },
        "double_thirds": {
            "thirds_frequency": 0.30,
            "note_density": 8.0
        },
        "advanced_chords": {
            "max_chord_size": 9,
            "note_density": 10.0
        },
        "advanced_counterpoint": {
            "poly_voice_count": 3,
            "left_hand_activity": 0.35,
            "polyrhythm_score": 0.25
        }
    },
    "5_labels": {
        "far_reach": {
            "max_stretch": 25,
            "octave_jump_frequency": 0.15
        },
        "double_thirds": {
            "thirds_frequency": 0.30,
            "note_density": 8.0
        },
        "multiple_voices": {
            "poly_voice_count": 3.5,
            "left_hand_activity": 0.40,
            "max_chord_size_max": 8  # Not too dense (that's Advanced Chords)
        },
        "advanced_chords": {
            "max_chord_size": 9,
            "note_density": 10.0
        },
        "advanced_counterpoint": {
            "poly_voice_count": 4,
            "left_hand_activity": 0.45,
            "polyrhythm_score": 0.30,
            "octave_jump_frequency": 0.20
        }
    }
}

# Default configuration
DEFAULT_CONFIG = "5_labels"  # Use 5 labels by default for better granularity


def get_labels(config_name=None):
    """Get label definitions for a configuration"""
    config_name = config_name or DEFAULT_CONFIG
    if config_name not in LABEL_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(LABEL_CONFIGS.keys())}")
    return LABEL_CONFIGS[config_name]


def get_num_classes(config_name=None):
    """Get number of classes for a configuration"""
    return len(get_labels(config_name))


def get_thresholds(config_name=None):
    """Get auto-labeling thresholds for a configuration"""
    config_name = config_name or DEFAULT_CONFIG
    if config_name not in AUTO_LABEL_THRESHOLDS:
        raise ValueError(f"Unknown config: {config_name}")
    return AUTO_LABEL_THRESHOLDS[config_name]


def get_label_name(label_id, config_name=None):
    """Get name for a specific label ID"""
    labels = get_labels(config_name)
    return labels.get(label_id, f"Unknown-{label_id}")


def get_config_info(config_name=None):
    """Get full information about a configuration"""
    config_name = config_name or DEFAULT_CONFIG
    return {
        "name": config_name,
        "num_classes": get_num_classes(config_name),
        "labels": get_labels(config_name),
        "thresholds": get_thresholds(config_name)
    }


# Category descriptions for documentation
CATEGORY_DESCRIPTIONS = {
    "4_labels": {
        0: "Wide hand spans and stretches (>25 semitones)",
        1: "Technical runs with frequent thirds intervals",
        2: "Dense chord textures (9+ notes)",
        3: "Complex voice independence and counterpoint"
    },
    "5_labels": {
        0: "Wide hand spans and stretches (>25 semitones)",
        1: "Technical runs with frequent thirds intervals",
        2: "Dense chord textures (9+ notes)",
        3: "Advanced counterpoint with voice independence and polyrhythms",
        4: "Polyphonic complexity with multiple independent voices"
    }
}


def print_config_summary(config_name=None):
    """Print a summary of the configuration"""
    config_name = config_name or DEFAULT_CONFIG
    info = get_config_info(config_name)
    descriptions = CATEGORY_DESCRIPTIONS[config_name]
    
    print(f"\n{'='*60}")
    print(f"Configuration: {config_name}")
    print(f"Number of Classes: {info['num_classes']}")
    print(f"{'='*60}\n")
    
    for label_id, label_name in info['labels'].items():
        print(f"{label_id}: {label_name}")
        print(f"   {descriptions[label_id]}")
        print()
