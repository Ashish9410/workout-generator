import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class WorkoutGenerator:
    def _init_(self):
        # Exercise database
        self.exercises = {
            "Chest": {
                "beginner": ["Push-ups", "Incline Push-ups", "Bench Press (light)", "Machine Chest Press", "Dumbbell Flyes"],
                "intermediate": ["Bench Press", "Incline Bench Press", "Dumbbell Press", "Cable Flyes", "Dips"],
                "advanced": ["Weighted Dips", "Decline Bench Press", "Dumbbell Pullovers", "Landmine Press", "Svend Press"]
            },
            "Back": {
                "beginner": ["Lat Pulldowns", "Seated Cable Rows", "Dumbbell Rows", "Assisted Pull-ups", "TRX Rows"],
                "intermediate": ["Pull-ups", "Barbell Rows", "T-Bar Rows", "Face Pulls", "Meadows Rows"],
                "advanced": ["Weighted Pull-ups", "Deadlifts", "Pendlay Rows", "Seal Rows", "Single-arm Dumbbell Rows"]
            },
            "Legs": {
                "beginner": ["Bodyweight Squats", "Leg Press", "Leg Extensions", "Leg Curls", "Calf Raises"],
                "intermediate": ["Barbell Squats", "Romanian Deadlifts", "Walking Lunges", "Bulgarian Split Squats", "Hack Squats"],
                "advanced": ["Front Squats", "Sumo Deadlifts", "Pistol Squats", "Barbell Hip Thrusts", "Deficit Lunges"]
            },
            "Shoulders": {
                "beginner": ["Dumbbell Lateral Raises", "Front Raises", "Face Pulls", "Machine Shoulder Press", "Shrugs"],
                "intermediate": ["Overhead Press", "Upright Rows", "Arnold Press", "Cable Lateral Raises", "Reverse Flyes"],
                "advanced": ["Push Press", "Single-arm Dumbbell Press", "Z-Press", "Handstand Push-ups", "Behind the Neck Press"]
            },
            "Arms": {
                "beginner": ["Dumbbell Curls", "Tricep Pushdowns", "Hammer Curls", "Tricep Kickbacks", "Concentration Curls"],
                "intermediate": ["Barbell Curls", "Skull Crushers", "Preacher Curls", "Dips", "Cable Curls"],
                "advanced": ["Weighted Chin-ups", "Close-grip Bench Press", "Spider Curls", "Overhead Tricep Extensions", "21s"]
            },
            "Core": {
                "beginner": ["Crunches", "Planks", "Russian Twists", "Leg Raises", "Mountain Climbers"],
                "intermediate": ["Hanging Leg Raises", "Cable Crunches", "Ab Wheel Rollouts", "Flutter Kicks", "Side Planks"],
                "advanced": ["Dragon Flags", "Toes to Bar", "Windshield Wipers", "L-Sits", "Weighted Planks"]
            }
        }
        
        # Specific exercises for different goals
        self.goal_specific_exercises = {
            "powerlifting": {
                "beginner": ["Squats", "Bench Press", "Deadlifts", "Romanian Deadlifts", "Overhead Press"],
                "intermediate": ["Box Squats", "Pause Bench Press", "Deficit Deadlifts", "Good Mornings", "Floor Press"],
                "advanced": ["Safety Bar Squats", "Board Press", "Rack Pulls", "Pause Squats", "Pin Press"]
            },
            "fat loss": {
                "beginner": ["Mountain Climbers", "Jumping Jacks", "Burpees", "High Knees", "Jump Rope"],
                "intermediate": ["Kettlebell Swings", "Battle Ropes", "Box Jumps", "Sledgehammer Slams", "Rowing Machine"],
                "advanced": ["Assault Bike", "Treadmill Sprints", "Prowler Push", "Ski Erg", "Complexes"]
            },
            "bodybuilding": {
                "beginner": ["Dumbbell Flyes", "Lateral Raises", "Concentration Curls", "Rope Pushdowns", "Machine Rows"],
                "intermediate": ["Incline DB Press", "Cable Crossovers", "Spider Curls", "Skull Crushers", "Pulldowns"],
                "advanced": ["Drop Sets", "Giant Sets", "Partial Reps", "Pre-exhaustion", "Supersets"]
            },
            "weightlifting": {
                "beginner": ["Clean Pull", "Overhead Squat", "Front Squat", "Push Press", "Power Clean"],
                "intermediate": ["Hang Clean", "Hang Snatch", "Split Jerk", "Clean and Jerk", "Power Snatch"],
                "advanced": ["Full Clean", "Full Snatch", "Jerk Dips", "Snatch Balance", "Clean Deadlift"]
            }
        }
        
        # Training splits templates
        self.training_splits = {
            "beginner": {
                "3-day": ["Full Body", "Rest", "Full Body", "Rest", "Full Body", "Rest", "Rest"],
                "4-day": ["Upper Body", "Lower Body", "Rest", "Upper Body", "Lower Body", "Rest", "Rest"],
                "5-day": ["Push", "Pull", "Legs", "Rest", "Upper Body", "Lower Body", "Rest"]
            },
            "intermediate": {
                "3-day": ["Push", "Pull", "Legs", "Rest", "Push", "Pull", "Rest"],
                "4-day": ["Upper Body", "Lower Body", "Rest", "Push", "Pull", "Legs", "Rest"],
                "5-day": ["Push", "Pull", "Legs", "Rest", "Upper Body", "Lower Body", "Rest"]
            },
            "advanced": {
                "3-day": ["Push/Pull", "Legs/Core", "Rest", "Push/Pull", "Legs/Core", "Upper Body", "Rest"],
                "4-day": ["Push", "Pull", "Rest", "Legs", "Upper Body", "Lower Body", "Rest"],
                "5-day": ["Push", "Pull", "Legs", "Rest", "Push", "Pull", "Legs"]
            },
            "powerlifting": {
                "3-day": ["Squat", "Bench", "Deadlift", "Rest", "Squat", "Bench", "Rest"],
                "4-day": ["Squat", "Bench", "Rest", "Deadlift", "Upper Body", "Lower Body", "Rest"],
                "5-day": ["Squat", "Bench", "Deadlift", "Rest", "Upper Body", "Lower Body", "Rest"]
            }
        }
    
    def calculate_calorie_needs(self, weight, height, age, gender, activity_level, goal):
        # Convert height from cm to meters
        height_m = height / 100
        
        # Calculate BMR using Mifflin-St Jeor Equation
        if gender.lower() == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:  # female
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multiplier
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly active": 1.375,
            "moderately active": 1.55,
            "very active": 1.725,
            "extra active": 1.9
        }
        
        tdee = bmr * activity_multipliers[activity_level.lower()]
        
        # Adjust based on goal
        goal_adjustments = {
            "fat loss": -500,  # Caloric deficit
            "maintenance": 0,
            "bodybuilding": 300,  # Caloric surplus
            "powerlifting": 500,  # Higher caloric surplus
            "weightlifting": 300
        }
        
        adjusted_calories = tdee + goal_adjustments.get(goal.lower(), 0)
        
        # Macronutrient breakdown
        protein_g = weight * 2.2  # 2.2g per kg of bodyweight
        
        if goal.lower() == "fat loss":
            fat_g = weight * 0.5  # 0.5g per kg of bodyweight
            # Remaining calories from carbs
            carb_g = (adjusted_calories - (protein_g * 4) - (fat_g * 9)) / 4
        elif goal.lower() in ["powerlifting", "weightlifting"]:
            carb_g = weight * 4  # 4g per kg of bodyweight
            # Remaining calories from fat
            fat_g = (adjusted_calories - (protein_g * 4) - (carb_g * 4)) / 9
        else:  # bodybuilding or maintenance
            fat_g = weight * 1  # 1g per kg of bodyweight
            # Remaining calories from carbs
            carb_g = (adjusted_calories - (protein_g * 4) - (fat_g * 9)) / 4
        
        return {
            "total_calories": round(adjusted_calories),
            "protein": round(protein_g),
            "carbs": round(carb_g),
            "fat": round(fat_g)
        }
    
    def generate_workout(self, experience_level, goal, gender, age, weight, height, days_per_week, activity_level):
        # Determine appropriate training split based on experience and days available
        if days_per_week <= 3:
            split_key = "3-day"
        elif days_per_week <= 4:
            split_key = "4-day"
        else:
            split_key = "5-day"
        
        # Use goal-specific split if available, otherwise use experience_level split
        if goal.lower() == "powerlifting" and goal.lower() in self.training_splits:
            weekly_split = self.training_splits[goal.lower()][split_key]
        else:
            weekly_split = self.training_splits[experience_level.lower()][split_key]
        
        # Trim the weekly split to match requested days per week
        weekly_split = weekly_split[:days_per_week] + ["Rest"] * (7 - days_per_week)
        
        # Generate workouts for each day
        workout_plan = {}
        for day_num, day_type in enumerate(weekly_split, 1):
            if day_type == "Rest":
                workout_plan[f"Day {day_num}"] = {"type": "Rest Day", "exercises": ["Active Recovery or Rest"]}
                continue
            
            # Initialize exercises list for this day
            day_exercises = []
            
            # Add specific exercises based on day type and goal
            if day_type in ["Push", "Pull", "Legs", "Upper Body", "Lower Body", "Full Body"]:
                # Map day types to body parts
                body_parts_map = {
                    "Push": ["Chest", "Shoulders", "Arms"],
                    "Pull": ["Back", "Arms"],
                    "Legs": ["Legs", "Core"],
                    "Upper Body": ["Chest", "Back", "Shoulders", "Arms"],
                    "Lower Body": ["Legs", "Core"],
                    "Full Body": ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core"]
                }
                
                selected_body_parts = body_parts_map[day_type]
                
                # Select 1-3 exercises per body part based on the day type
                for body_part in selected_body_parts:
                    num_exercises = 3 if day_type == "Full Body" else (2 if day_type in ["Upper Body", "Lower Body"] else 3)
                    
                    available_exercises = self.exercises[body_part][experience_level.lower()]
                    selected_exercises = random.sample(available_exercises, min(num_exercises, len(available_exercises)))
                    
                    for exercise in selected_exercises:
                        # Determine sets and reps based on experience and goal
                        if goal.lower() == "powerlifting":
                            sets = random.randint(4, 5) if experience_level.lower() != "beginner" else random.randint(3, 4)
                            reps = f"{random.randint(3, 5)}" if experience_level.lower() == "advanced" else f"{random.randint(4, 6)}"
                        elif goal.lower() == "fat loss":
                            sets = random.randint(3, 4)
                            reps = f"{random.randint(12, 15)}" if experience_level.lower() == "beginner" else f"{random.randint(10, 15)}"
                        elif goal.lower() == "bodybuilding":
                            sets = random.randint(3, 4) if experience_level.lower() == "beginner" else random.randint(4, 5)
                            reps = f"{random.randint(8, 12)}"
                        else:  # weightlifting
                            sets = random.randint(4, 5)
                            reps = f"{random.randint(3, 5)}" if experience_level.lower() == "advanced" else f"{random.randint(5, 8)}"
                        
                        day_exercises.append({
                            "name": exercise,
                            "sets": sets,
                            "reps": reps,
                            "rest": f"{60 if goal.lower() == 'fat loss' else (180 if goal.lower() == 'powerlifting' else 90)} sec"
                        })
            
            # For specialized day types (Squat, Bench, Deadlift days in powerlifting)
            elif goal.lower() == "powerlifting":
                if day_type == "Squat":
                    main_exercises = ["Squats", "Box Squats"] if experience_level.lower() != "beginner" else ["Squats"]
                    accessory_exercises = ["Leg Press", "Romanian Deadlifts", "Bulgarian Split Squats", "Good Mornings"]
                elif day_type == "Bench":
                    main_exercises = ["Bench Press", "Close-grip Bench Press"] if experience_level.lower() != "beginner" else ["Bench Press"]
                    accessory_exercises = ["Dumbbell Press", "Tricep Extensions", "Dips", "Cable Flyes"]
                elif day_type == "Deadlift":
                    main_exercises = ["Deadlifts", "Deficit Deadlifts"] if experience_level.lower() != "beginner" else ["Deadlifts"]
                    accessory_exercises = ["Pull-ups", "Barbell Rows", "Lat Pulldowns", "Face Pulls"]
                
                # Add main exercise
                for exercise in main_exercises:
                    sets = random.randint(4, 5) if experience_level.lower() != "beginner" else random.randint(3, 4)
                    reps = f"{random.randint(3, 5)}" if experience_level.lower() == "advanced" else f"{random.randint(4, 6)}"
                    day_exercises.append({
                        "name": exercise,
                        "sets": sets,
                        "reps": reps,
                        "rest": "180-240 sec"
                    })
                
                # Add 2-3 accessory exercises
                selected_accessories = random.sample(accessory_exercises, random.randint(2, 3))
                for exercise in selected_accessories:
                    sets = random.randint(3, 4)
                    reps = f"{random.randint(8, 12)}"
                    day_exercises.append({
                        "name": exercise,
                        "sets": sets,
                        "reps": reps,
                        "rest": "90-120 sec"
                    })
            
            # Add workout details
            workout_plan[f"Day {day_num}"] = {
                "type": day_type,
                "exercises": day_exercises
            }
        
        # Calculate calorie needs
        nutrition_plan = self.calculate_calorie_needs(weight, height, age, gender, activity_level, goal)
        
        # Compile full plan with workout and nutrition
        full_plan = {
            "personal_info": {
                "gender": gender,
                "age": age,
                "weight": weight,
                "height": height,
                "experience_level": experience_level,
                "goal": goal,
                "activity_level": activity_level
            },
            "workout_plan": workout_plan,
            "nutrition_plan": nutrition_plan,
            "recommendations": self.get_recommendations(experience_level, goal)
        }
        
        return full_plan
    
    def get_recommendations(self, experience_level, goal):
        recommendations = {
            "beginner": {
                "general": "Focus on learning proper technique before adding heavy weight.",
                "recovery": "Make sure to get 7-9 hours of sleep and stay well hydrated.",
                "progression": "Aim to add small amounts of weight each week or increase reps."
            },
            "intermediate": {
                "general": "Consider tracking your workouts to ensure progressive overload.",
                "recovery": "Pay attention to proper warm-up and cool-down routines.",
                "progression": "Implement deload weeks every 4-6 weeks of training."
            },
            "advanced": {
                "general": "Consider periodization in your training for continued progress.",
                "recovery": "Recovery modalities like massage, contrast baths may be beneficial.",
                "progression": "Focus on weak points and implement specialized techniques."
            }
        }
        
        goal_specific = {
            "powerlifting": "Emphasize the big three lifts: squat, bench press, and deadlift. Focus on strength in the 1-5 rep range.",
            "fat loss": "Combine resistance training with some cardio. Keep rest periods shorter and consider circuit training.",
            "bodybuilding": "Focus on mind-muscle connection, proper form, and target all muscle groups for balanced development.",
            "weightlifting": "Practice Olympic lift technique frequently. Focus on mobility, especially in ankles, hips, and shoulders."
        }
        
        result = recommendations[experience_level.lower()]
        result["goal_specific"] = goal_specific[goal.lower()]
        
        return result


class WorkoutGeneratorApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Personalized Workout Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize the workout generator
        self.generator = WorkoutGenerator()
        
        # Create a main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.input_tab = ttk.Frame(self.notebook)
        self.result_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.input_tab, text="Input Parameters")
        self.notebook.add(self.result_tab, text="Workout Plan")
        
        # Setup the input form
        self.setup_input_form()
        
        # Setup the results view (initially empty)
        self.setup_results_view()
        
        # Save/Load features
        self.setup_save_load_buttons(main_frame)
        
    def setup_input_form(self):
        # Create a frame for the input form with scrollbar
        canvas = tk.Canvas(self.input_tab)
        scrollbar = ttk.Scrollbar(self.input_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        ttk.Label(scrollable_frame, text="Create Your Personalized Workout Plan", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20, sticky="w")
        
        # Personal Info Section
        ttk.Label(scrollable_frame, text="Personal Information", font=("Helvetica", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        # Gender
        ttk.Label(scrollable_frame, text="Gender:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = ttk.Frame(scrollable_frame)
        gender_frame.grid(row=2, column=1, pady=5, sticky="w")
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT, padx=5)
        
        # Age
        ttk.Label(scrollable_frame, text="Age (years):").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.age_var = tk.IntVar(value=30)
        ttk.Spinbox(scrollable_frame, from_=15, to=80, textvariable=self.age_var, width=10).grid(row=3, column=1, pady=5, sticky="w")
        
        # Weight
        ttk.Label(scrollable_frame, text="Weight (kg):").grid(row=4, column=0, pady=5, padx=5, sticky="w")
        self.weight_var = tk.IntVar(value=70)
        ttk.Spinbox(scrollable_frame, from_=40, to=200, textvariable=self.weight_var, width=10).grid(row=4, column=1, pady=5, sticky="w")
        
        # Height
        ttk.Label(scrollable_frame, text="Height (cm):").grid(row=5, column=0, pady=5, padx=5, sticky="w")
        self.height_var = tk.IntVar(value=170)
        ttk.Spinbox(scrollable_frame, from_=140, to=220, textvariable=self.height_var, width=10).grid(row=5, column=1, pady=5, sticky="w")
        
        # Activity Level
        ttk.Label(scrollable_frame, text="Activity Level:").grid(row=6, column=0, pady=5, padx=5, sticky="w")
        self.activity_var = tk.StringVar(value="Moderately Active")
        ttk.Combobox(scrollable_frame, textvariable=self.activity_var, width=20, 
                     values=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]).grid(row=6, column=1, pady=5, sticky="w")
        
        # Workout Parameters Section
        ttk.Label(scrollable_frame, text="Workout Parameters", font=("Helvetica", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        # Experience Level
        ttk.Label(scrollable_frame, text="Experience Level:").grid(row=8, column=0, pady=5, padx=5, sticky="w")
        self.experience_var = tk.StringVar(value="Beginner")
        ttk.Combobox(scrollable_frame, textvariable=self.experience_var, width=20, 
                     values=["Beginner", "Intermediate", "Advanced"]).grid(row=8, column=1, pady=5, sticky="w")
        
        # Workout Goal
        ttk.Label(scrollable_frame, text="Workout Goal:").grid(row=9, column=0, pady=5, padx=5, sticky="w")
        self.goal_var = tk.StringVar(value="Bodybuilding")
        ttk.Combobox(scrollable_frame, textvariable=self.goal_var, width=20, 
                     values=["Powerlifting", "Fat Loss", "Bodybuilding", "Weightlifting"]).grid(row=9, column=1, pady=5, sticky="w")
        
        # Days per week
        ttk.Label(scrollable_frame, text="Days per Week:").grid(row=10, column=0, pady=5, padx=5, sticky="w")
        self.days_var = tk.IntVar(value=4)
        ttk.Spinbox(scrollable_frame, from_=3, to=6, textvariable=self.days_var, width=10).grid(row=10, column=1, pady=5, sticky="w")
        
        # Generate button
        generate_btn = ttk.Button(scrollable_frame, text="Generate Workout Plan", command=self.generate_workout)
        generate_btn.grid(row=11, column=0, columnspan=2, pady=20)
        
    def setup_results_view(self):
        # Create a frame with scrollbar for results
        canvas = tk.Canvas(self.result_tab)
        scrollbar = ttk.Scrollbar(self.result_tab, orient="vertical", command=canvas.yview)
        self.results_frame = ttk.Frame(canvas)
        
        self.results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        ttk.Label(self.results_frame, text="Your workout plan will appear here after generation", 
                 font=("Helvetica", 12)).grid(row=0, column=0, pady=20)
    
    def setup_save_load_buttons(self, parent_frame):
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Save Workout Plan", command=self.save_workout).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Workout Plan", command=self.load_workout).pack(side=tk.LEFT, padx=5)
    
    def generate_workout(self):
        try:
            # Get input values
            experience_level = self.experience_var.get()
            goal = self.goal_var.get()
            gender = self.gender_var.get()
            age = self.age_var.get()
            weight = self.weight_var.get()
            height = self.height_var.get()
            days_per_week = self.days_var.get()
            activity_level = self.activity_var.get()
            
            # Generate workout plan
            self.workout_plan = self.generator.generate_workout(
                experience_level, goal, gender, age, weight, height, days_per_week, activity_level
            )
            
            # Display results
            self.display_workout_plan(self.workout_plan)
            
            # Switch to results tab
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_workout_plan(self, plan):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Title
        ttk.Label(self.results_frame, text="Your Personalized Workout Plan", 
                 font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20, sticky="w")
        
        # Personal Info Section
        ttk.Label(self.results_frame, text="Personal Information", 
                 font=("Helvetica", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=(10, 5), sticky="w")
        
        info = plan["personal_info"]
        info_text = f"Gender: {info['gender']} | Age: {info['age']} | Weight: {info['weight']}kg | Height: {info['height']}cm\n"
        info_text += f"Experience Level: {info['experience_level']} | Goal: {info['goal']} | Activity Level: {info['activity_level']}"
        
        ttk.Label(self.results_frame, text=info_text, wraplength=800).grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
        
        # Nutrition Plan Section
        ttk.Label(self.results_frame, text="Nutrition Plan", 
                 font=("Helvetica", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky="w")
        
        nutrition = plan["nutrition_plan"]
        nutrition_text = f"Daily Calories: {nutrition['total_calories']} kcal\n"
        nutrition_text += f"Protein: {nutrition['protein']}g ({round(nutrition['protein']*4)}kcal)\n"
        nutrition_text += f"Carbs: {nutrition['carbs']}g ({round(nutrition['carbs']*4)}kcal)\n"
        nutrition_text += f"Fat: {nutrition['fat']}g ({round(nutrition['fat']*9)}kcal)"
        
        ttk.Label(self.results_frame, text=nutrition_text).grid(row=4, column=0, columnspan=2, pady=5, sticky="w")
        
        # Workout Plan Section
        ttk.Label(self.results_frame, text="Weekly Workout Schedule", 
                 font=("Helvetica", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        # Create a frame for the workout tabs
        workout_notebook = ttk.Notebook(self.results_frame)
        workout_notebook.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Create tabs for each workout day
        for day, workout in plan["workout_plan"].items():
            day_frame = ttk.Frame(workout_notebook)
            workout_notebook.add(day_frame, text=day)
            
            # Day type label
            ttk.Label(day_frame, text=f"Training Focus: {workout['type']}", 
                     font=("Helvetica", 10, "bold")).grid(row=0, column=0, columnspan=5, pady=10, sticky="w")
            
            # Headers
            ttk.Label(day_frame, text="Exercise", font=("Helvetica", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
            ttk.Label(day_frame, text="Sets", font=("Helvetica", 10, "bold")).grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(day_frame, text="Reps", font=("Helvetica", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
            ttk.Label(day_frame, text="Rest", font=("Helvetica", 10, "bold")).grid(row=1, column=3, padx=5, pady=5)
            
            # Exercise rows
            if workout["type"] == "Rest Day":
                ttk.Label(day_frame, text="Rest or Light Activity", font=("Helvetica", 10, "italic")).grid(
                    row=2, column=0, columnspan=4, padx=5, pady=10)
            else:
                for i, exercise in enumerate(workout["exercises"], 2):
                    if isinstance(exercise, dict):  # Check if it's a structured exercise
                        ttk.Label(day_frame, text=exercise["name"]).grid(row=i, column=0, padx=5, pady=3, sticky="w")
                        ttk.Label(day_frame, text=str(exercise["sets"])).grid(row=i, column=1, padx=5, pady=3)
                        ttk.Label(day_frame, text=str(exercise["reps"])).grid(row=i, column=2, padx=5, pady=3)
                        ttk.Label(day_frame, text=str(exercise["rest"])).grid(row=i, column=3, padx=5, pady=3)
                    else:  # It's just a string (like for rest days)
                        ttk.Label(day_frame, text=exercise).grid(row=i, column=0, columnspan=4, padx=5, pady=3, sticky="w")
        
        # Recommendations Section
        ttk.Label(self.results_frame, text="Recommendations", 
                 font=("Helvetica", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        recommendations = plan["recommendations"]
        
        rec_frame = ttk.Frame(self.results_frame)
        rec_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5)
        
        ttk.Label(rec_frame, text="General Advice:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(rec_frame, text=recommendations["general"], wraplength=800).grid(row=0, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(rec_frame, text="Recovery Tips:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(rec_frame, text=recommendations["recovery"], wraplength=800).grid(row=1, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(rec_frame, text="Progression:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(rec_frame, text=recommendations["progression"], wraplength=800).grid(row=2, column=1, sticky="w", pady=2, padx=5)
        
        ttk.Label(rec_frame, text="Goal-Specific:", font=("Helvetica", 10, "bold")).grid(row=3, column=0, sticky="w", pady=2)
        ttk.Label(rec_frame, text=recommendations["goal_specific"], wraplength=800).grid(row=3, column=1, sticky="w", pady=2, padx=5)
        
    def save_workout(self):
        if not hasattr(self, 'workout_plan'):
            messagebox.showinfo("Info", "Please generate a workout plan first.")
            return
            
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", ".json"), ("All files", ".*")],
            title="Save Workout Plan"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.workout_plan, f, indent=4)
                messagebox.showinfo("Success", "Workout plan saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save workout plan: {str(e)}")
    
    def load_workout(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[("JSON files", ".json"), ("All files", ".*")],
            title="Load Workout Plan"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    workout_plan = json.load(f)
                
                self.workout_plan = workout_plan
                self.display_workout_plan(workout_plan)
                self.notebook.select(1)  # Switch to results tab
                messagebox.showinfo("Success", "Workout plan loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load workout plan: {str(e)}")


if name == "_main_":
    root = tk.Tk()
    app = WorkoutGeneratorApp(root)
    root.mainloop()