"""
add_authentic_indian_recipes.py
-------------------------------
Adds authentic, everyday South Indian and North Indian recipes
(Sambar, Chutney, Rasam, Dosa, Biryani, Curries, Poriyal, etc.)
to data/processed_recipes.csv so that everyday home-cooking ingredients
yield realistic, accurate, and recognizable Indian dishes.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_CSV_PATH = os.path.join(BASE_DIR, "data", "processed_recipes.csv")

# Curated authentic everyday Indian recipes
AUTHENTIC_RECIPES = [
    # ==================== SAMBAR VARIETIES ====================
    {
        "recipe_name": "Traditional South Indian Drumstick Sambar (Murungakkai Sambar)",
        "cleaned_ingredients": "toor dal, drumstick, tomato, onion, tamarind, sambar powder, turmeric, mustard, curry leaf, coriander, asafoetida, salt, oil",
        "ingredients_raw": "- 1 cup Toor Dal (Arhar Dal)\n- 2 Drumsticks (cut into 2-inch pieces)\n- 1 medium Onion or Shallots (sliced)\n- 2 medium Tomatoes (chopped)\n- 1 small lemon-sized Tamarind (soaked in warm water)\n- 2 tbsp Sambar Powder\n- 1/2 tsp Turmeric Powder\n- 1 tsp Mustard Seeds\n- 1 sprig fresh Curry Leaves\n- 2 tbsp fresh Coriander Leaves\n- 1/4 tsp Asafoetida (Hing)\n- Salt to taste\n- 1 tbsp Cooking Oil or Ghee",
        "instructions": "1. Pressure cook toor dal with a pinch of turmeric and 3 cups of water for 4 whistles until soft and mushy.\n2. In a heavy pot, heat oil, add mustard seeds, asafoetida, and curry leaves; let them crackle.\n3. Add sliced onions and sauté until translucent, then add tomatoes and cook until soft.\n4. Add drumstick pieces, tamarind water, sambar powder, turmeric, salt, and 1.5 cups of water. Cover and boil until drumsticks are tender (about 8-10 mins).\n5. Pour in the cooked mashed toor dal, mix well, and simmer on medium flame for 5 minutes until flavors blend.\n6. Garnish with fresh chopped coriander leaves and serve piping hot with steamed rice and ghee or idli/dosa!",
        "total_time": 30,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Madras Hotel Style Tiffin Sambar (for Idli & Dosa)",
        "cleaned_ingredients": "toor dal, moong dal, shallot, tomato, carrot, sambar powder, tamarind, mustard, curry leaf, asafoetida, ghee, coriander, salt",
        "ingredients_raw": "- 1/2 cup Toor Dal\n- 1/4 cup Yellow Moong Dal\n- 10-12 Small Onions (Shallots / Chinna Vengayam)\n- 2 ripe Tomatoes (finely chopped)\n- 1 medium Carrot (diced)\n- 2 tbsp Sambar Powder\n- 1 tbsp Tamarind extract\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- 1/4 tsp Asafoetida (Hing)\n- 1 tbsp Ghee or Oil\n- 2 tbsp fresh Coriander Leaves\n- Salt to taste",
        "instructions": "1. Pressure cook toor dal and moong dal together with turmeric and 2.5 cups of water until completely soft; mash smoothly.\n2. In a pot, heat ghee, crackle mustard seeds, asafoetida, and curry leaves.\n3. Add whole peeled shallots and sauté for 3 minutes until aromatic. Add chopped tomatoes and carrot; cook for 3 minutes.\n4. Add tamarind water, sambar powder, salt, and 1 cup of water. Simmer until carrots and onions are cooked.\n5. Add the mashed dal mixture, adjust consistency with water, and let it come to a rolling boil for 4-5 minutes.\n6. Finish with fresh coriander leaves. Serve hot with fluffy idlis, crispy dosas, or medu vada!",
        "total_time": 25,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Classic Tomato Onion Sambar (Thakkali Vengaya Sambar)",
        "cleaned_ingredients": "toor dal, tomato, onion, tamarind, sambar powder, turmeric, mustard, curry leaf, green chilli, coriander, salt, oil",
        "ingredients_raw": "- 3/4 cup Toor Dal\n- 3 large ripe Tomatoes (chopped)\n- 1 large Onion (thinly sliced)\n- 2 Green Chillies (slit)\n- 1 tbsp Tamarind extract\n- 2 tbsp Sambar Powder\n- 1/2 tsp Turmeric Powder\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- 2 tbsp Coriander Leaves\n- Salt to taste\n- 1 tbsp Oil",
        "instructions": "1. Pressure cook toor dal with turmeric until soft and mash well.\n2. Heat oil in a pan, add mustard seeds and curry leaves.\n3. Add sliced onions and slit green chillies; sauté until onions turn translucent.\n4. Add chopped tomatoes, sambar powder, salt, and tamarind water. Cook on medium heat until tomatoes become soft and pulpy.\n5. Add the mashed dal and 1 cup of water; simmer on medium flame for 5 minutes.\n6. Garnish with chopped coriander and serve hot with steamed rice.",
        "total_time": 25,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Mixed Vegetable Sambar",
        "cleaned_ingredients": "toor dal, carrot, potato, tomato, onion, drumstick, tamarind, sambar powder, mustard, curry leaf, asafoetida, salt, oil",
        "ingredients_raw": "- 1 cup Toor Dal\n- 1 Carrot (diced)\n- 1 Potato (cubed)\n- 1 Drumstick (cut into pieces)\n- 1 Onion (sliced)\n- 2 Tomatoes (chopped)\n- 1.5 tbsp Tamarind extract\n- 2.5 tbsp Sambar Powder\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- 1/4 tsp Asafoetida\n- Salt to taste\n- 1 tbsp Oil",
        "instructions": "1. Pressure cook toor dal until soft and mash smooth.\n2. In a large cooking pot, boil carrot, potato, drumstick, onion, and tomatoes with tamarind water, sambar powder, salt, and 2 cups of water until vegetables are fork-tender.\n3. Add the mashed dal and simmer for 5-6 minutes on medium heat.\n4. In a small seasoning pan, heat oil, add mustard seeds, asafoetida, and curry leaves until fragrant.\n5. Pour the tempering into the sambar, stir well, and serve hot.",
        "total_time": 30,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },

    # ==================== CHUTNEY VARIETIES ====================
    {
        "recipe_name": "Hotel Style White Coconut Chutney (Thengai Chutney)",
        "cleaned_ingredients": "coconut, green chilli, chana dal, ginger, salt, mustard, urad dal, curry leaf, oil",
        "ingredients_raw": "- 1 cup freshly grated Coconut\n- 2-3 Green Chillies\n- 2 tbsp Roasted Gram / Chana Dal (Pottukadalai)\n- 1/2 inch piece Ginger\n- Salt to taste\n- 1 tsp Mustard Seeds\n- 1 tsp Urad Dal\n- 1 sprig fresh Curry Leaves\n- 1 tsp Cooking Oil",
        "instructions": "1. In a blender, combine grated coconut, green chillies, roasted gram (pottukadalai), ginger, and salt.\n2. Add about 1/4 to 1/2 cup of water and grind into a smooth or slightly coarse paste.\n3. Transfer chutney to a serving bowl.\n4. Heat 1 tsp oil in a tadka pan. Add mustard seeds, urad dal, and curry leaves; let the mustard crackle and urad dal turn golden brown.\n5. Pour the hot tempering over the chutney, mix well, and serve with hot idli, crispy dosa, or vadai!",
        "total_time": 10,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Spicy Tomato Onion Chutney (Thakkali Vengaya Chutney)",
        "cleaned_ingredients": "tomato, onion, garlic, red chilli, urad dal, mustard, curry leaf, salt, oil",
        "ingredients_raw": "- 2 large ripe Tomatoes (chopped)\n- 1 large Onion (chopped)\n- 4-5 cloves Garlic\n- 3-4 Dry Red Chillies\n- 1 tbsp Urad Dal\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- Salt to taste\n- 1.5 tbsp Sesame Oil or Cooking Oil",
        "instructions": "1. Heat 1 tbsp oil in a pan. Add urad dal and dry red chillies; roast on low flame until dal turns golden.\n2. Add garlic cloves and chopped onions; sauté until onions become light golden and soft.\n3. Add chopped tomatoes and salt; cook on medium flame until tomatoes are mushy and oil leaves the sides.\n4. Remove from heat and let the mixture cool completely.\n5. Transfer to a mixer jar and grind into a smooth chutney with minimal water.\n6. Temper with mustard seeds and curry leaves in hot oil; mix into the chutney. Delicious with dosa, idli, and uthappam!",
        "total_time": 15,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Chettinad Kara Chutney (Red Spicy Chutney)",
        "cleaned_ingredients": "onion, tomato, garlic, red chilli, tamarind, mustard, curry leaf, salt, sesame oil",
        "ingredients_raw": "- 2 medium Onions (chopped)\n- 2 medium Tomatoes (chopped)\n- 6-7 cloves Garlic\n- 5-6 Dry Red Chillies\n- 1 small piece Tamarind\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Gingelly / Sesame Oil",
        "instructions": "1. Heat 1 tbsp sesame oil in a pan; add dry red chillies and garlic, sauté for 1 minute.\n2. Add onions and sauté until translucent.\n3. Add tomatoes, tamarind, and salt; cook until tomatoes turn soft and tender.\n4. Cool and grind into a slightly thick, smooth chutney.\n5. Heat remaining sesame oil, crackle mustard seeds and curry leaves, and pour over the chutney. Ideal for crispy dosas and idlis!",
        "total_time": 15,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Chettinad"
    },
    {
        "recipe_name": "Fresh Mint & Coriander Chutney (Pudina Kothamalli Chutney)",
        "cleaned_ingredients": "mint, coriander, green chilli, ginger, coconut, chana dal, salt, lemon juice",
        "ingredients_raw": "- 1 cup fresh Mint Leaves (Pudina)\n- 1 cup fresh Coriander Leaves (Dhania)\n- 2 Green Chillies\n- 1/2 inch Ginger\n- 2 tbsp grated Coconut\n- 1 tbsp Roasted Chana Dal\n- 1 tbsp Lemon Juice\n- Salt to taste",
        "instructions": "1. Wash mint and coriander leaves thoroughly in fresh water.\n2. Place mint, coriander, green chillies, ginger, coconut, roasted chana dal, and salt in a blender.\n3. Add 2-3 tablespoons of water and blend to a smooth, vibrant green chutney.\n4. Stir in fresh lemon juice for brightness and tang. Perfect for samosas, sandwiches, dosas, and chaat!",
        "total_time": 10,
        "meal_type": "Snack",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },

    # ==================== RASAM VARIETIES ====================
    {
        "recipe_name": "Classic Tomato Pepper Rasam (Thakkali Milagu Rasam)",
        "cleaned_ingredients": "tomato, pepper, cumin, garlic, tamarind, mustard, curry leaf, coriander, turmeric, asafoetida, salt, ghee",
        "ingredients_raw": "- 3 ripe Tomatoes (crushed by hand)\n- 1 tsp Black Peppercorns\n- 1 tsp Cumin Seeds (Jeera)\n- 5 cloves Garlic (crushed)\n- 1 small marble-sized Tamarind (soaked in 1 cup warm water)\n- 1/2 tsp Turmeric Powder\n- 1/4 tsp Asafoetida (Hing)\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- 2 tbsp fresh Coriander Leaves\n- 1 tsp Ghee or Oil\n- Salt to taste",
        "instructions": "1. Coarsely crush black peppercorns, cumin seeds, and garlic cloves using a mortar-pestle.\n2. In a pot, combine crushed tomatoes, tamarind water, turmeric, salt, asafoetida, and 1.5 cups of water. Boil for 6-7 minutes until raw tamarind aroma disappears.\n3. Add the crushed pepper-cumin-garlic mixture and simmer gently until a frothy layer forms on top (do not let it boil vigorously).\n4. In a small pan, heat ghee, add mustard seeds and curry leaves until they crackle.\n5. Pour the hot tempering over the rasam, garnish generously with fresh coriander, cover with a lid immediately to trap the aroma, and serve hot with rice!",
        "total_time": 15,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Poondu Rasam (Spicy Garlic Rasam)",
        "cleaned_ingredients": "garlic, pepper, cumin, tomato, tamarind, mustard, curry leaf, coriander, turmeric, salt, ghee",
        "ingredients_raw": "- 10-12 cloves Garlic (peeled and lightly crushed)\n- 1.5 tsp Black Pepper\n- 1 tsp Cumin Seeds\n- 1 large Tomato (chopped)\n- 1 tbsp Tamarind extract\n- 1/2 tsp Turmeric Powder\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- 2 tbsp Coriander Leaves\n- Salt to taste\n- 1 tbsp Ghee",
        "instructions": "1. Crush black pepper and cumin coarsely; crush garlic cloves.\n2. Heat ghee in a pot, add mustard seeds, curry leaves, and crushed garlic; sauté until garlic turns light golden and aromatic.\n3. Add chopped tomato, tamarind water, turmeric, salt, and 2 cups of water.\n4. Bring to a gentle simmer for 5 minutes, then add the crushed pepper-cumin.\n5. Turn off the flame when frothy, garnish with coriander leaves, and enjoy hot!",
        "total_time": 15,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },

    # ==================== TIFFIN & BREAKFAST ====================
    {
        "recipe_name": "Crispy Golden Plain Dosa",
        "cleaned_ingredients": "rice, urad dal, fenugreek, salt, oil",
        "ingredients_raw": "- 3 cups Idli / Dosa Rice\n- 1 cup Whole Urad Dal\n- 1/2 tsp Fenugreek Seeds (Methi)\n- Salt to taste\n- Oil or Ghee for making dosas",
        "instructions": "1. Wash and soak rice and fenugreek seeds in one bowl, and urad dal in another bowl for 4-5 hours.\n2. Grind urad dal until light and fluffy; grind rice until smooth. Mix both batters together with salt and ferment overnight (8 hours).\n3. Heat a flat tawa or griddle. Pour a ladleful of batter in the center and spread outward in a spiral to form a thin crepe.\n4. Drizzle a teaspoon of oil around the edges and cook on medium-high flame until edges lift and turn golden-brown and crispy.\n5. Fold and serve hot with Coconut Chutney and Sambar!",
        "total_time": 20,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Soft Spongy Idli",
        "cleaned_ingredients": "rice, urad dal, fenugreek, salt, water",
        "ingredients_raw": "- 4 cups Idli Rice\n- 1 cup Whole Urad Dal\n- 1/2 tsp Fenugreek Seeds\n- Salt to taste\n- Water as needed",
        "instructions": "1. Soak rice and urad dal separately for 4-5 hours.\n2. Grind urad dal to a very fluffy, light consistency. Grind rice to a slightly coarse, smooth paste.\n3. Combine both with salt and allow to ferment in a warm place for 8-10 hours until batter doubles in volume.\n4. Grease idli plates with oil, gently pour batter into molds without deflating.\n5. Steam in an idli pot or steamer for 10-12 minutes on high flame.\n6. Let cool for 2 minutes, scoop out with a wet spoon, and serve hot with Sambar and Chutney!",
        "total_time": 20,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Traditional South Indian Ven Pongal",
        "cleaned_ingredients": "rice, moong dal, pepper, cumin, ginger, cashew, curry leaf, asafoetida, ghee, salt",
        "ingredients_raw": "- 1 cup Raw Rice\n- 1/2 cup Yellow Moong Dal\n- 1 tsp whole Black Peppercorns\n- 1 tsp Cumin Seeds\n- 1 inch Ginger (finely chopped)\n- 10-12 Cashews\n- 1 sprig Curry Leaves\n- 1/4 tsp Asafoetida\n- 3-4 tbsp Ghee\n- Salt to taste",
        "instructions": "1. Dry roast moong dal in a pan on medium heat until fragrant (about 2-3 mins).\n2. Wash rice and roasted dal together. Pressure cook with 4.5 cups of water and salt for 4-5 whistles until very soft and mushy.\n3. In a pan, heat ghee generously. Add cashews and fry until golden; remove cashews and set aside.\n4. In the same hot ghee, add cumin seeds, black peppercorns, chopped ginger, asafoetida, and curry leaves; sauté until aromatic.\n5. Pour the hot tempering and fried cashews over the mashed rice-dal mixture and stir well.\n6. Serve piping hot with Coconut Chutney and Sambar!",
        "total_time": 25,
        "meal_type": "Breakfast",
        "diet": "Vegetarian",
        "servings": 4,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Crispy Medu Vada (Ulundu Vadai)",
        "cleaned_ingredients": "urad dal, onion, green chilli, ginger, pepper, curry leaf, asafoetida, salt, oil",
        "ingredients_raw": "- 1 cup Whole White Urad Dal\n- 1 small Onion (finely chopped)\n- 2 Green Chillies (finely chopped)\n- 1 inch Ginger (minced)\n- 1 tsp Black Peppercorns (crushed)\n- 1 sprig Curry Leaves (chopped)\n- 1/4 tsp Asafoetida\n- Salt to taste\n- Oil for deep frying",
        "instructions": "1. Soak urad dal for 2 hours. Drain completely and grind with 2-3 tablespoons of ice-cold water into a thick, fluffy batter.\n2. Beat the batter with your hands for 2 minutes to incorporate air until light.\n3. Add chopped onions, green chillies, ginger, crushed pepper, curry leaves, asafoetida, and salt; mix gently.\n4. Wet your hands with water, take a small portion of batter, flatten on your palm, make a hole in the center with your thumb.\n5. Slide gently into hot oil and deep fry on medium flame until golden brown and crispy on both sides.\n6. Drain on paper towels and serve crispy vadas with hot Sambar and Coconut Chutney!",
        "total_time": 30,
        "meal_type": "Snack",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Medium",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },

    # ==================== RICE VARIETIES ====================
    {
        "recipe_name": "South Indian Curd Rice (Thayir Sadam)",
        "cleaned_ingredients": "rice, curd, milk, mustard, green chilli, ginger, curry leaf, coriander, asafoetida, salt, oil",
        "ingredients_raw": "- 1 cup cooked Rice (soft and slightly mashed)\n- 1 cup fresh thick Curd (Yogurt)\n- 1/4 cup Milk\n- 1 tsp Mustard Seeds\n- 1-2 Green Chillies (slit)\n- 1/2 inch Ginger (finely chopped)\n- 1 sprig Curry Leaves\n- 1 tbsp Coriander Leaves\n- 1/4 tsp Asafoetida\n- Salt to taste\n- 1 tsp Oil",
        "instructions": "1. Mash warm cooked rice well in a mixing bowl; let it cool slightly.\n2. Add fresh curd, milk, and salt; mix thoroughly until creamy.\n3. Heat oil in a tadka pan, crackle mustard seeds, add green chillies, ginger, curry leaves, and asafoetida.\n4. Pour the tempering over the curd rice and mix well.\n5. Garnish with fresh coriander leaves (and optional pomegranate seeds). Serve cool with pickle!",
        "total_time": 15,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 2,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "South Indian Lemon Rice (Elumichai Sadam)",
        "cleaned_ingredients": "rice, lemon juice, turmeric, mustard, urad dal, chana dal, peanut, green chilli, ginger, curry leaf, salt, oil",
        "ingredients_raw": "- 2 cups cooked cooled Rice\n- 2 tbsp fresh Lemon Juice\n- 1/2 tsp Turmeric Powder\n- 1 tsp Mustard Seeds\n- 1 tsp Urad Dal\n- 1 tsp Chana Dal\n- 2 tbsp raw Peanuts\n- 2 Green Chillies (slit)\n- 1/2 inch Ginger (grated)\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Sesame Oil or Cooking Oil",
        "instructions": "1. Heat oil in a pan, add peanuts and roast on low flame until crunchy.\n2. Add mustard seeds, urad dal, chana dal; let mustard pop and dals turn golden brown.\n3. Add slit green chillies, ginger, curry leaves, turmeric powder, and salt; sauté for 30 seconds.\n4. Turn off the flame and stir in fresh lemon juice.\n5. Gently fold in the cooked rice until every grain is coated in the vibrant yellow seasoning. Serve with potato fry or papad!",
        "total_time": 15,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 2,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },
    {
        "recipe_name": "Spicy Tomato Rice (Thakkali Sadam)",
        "cleaned_ingredients": "rice, tomato, onion, ginger, garlic, green chilli, red chilli powder, turmeric, mustard, curry leaf, salt, oil",
        "ingredients_raw": "- 2 cups cooked Rice (cooled)\n- 3 large ripe Tomatoes (finely chopped)\n- 1 large Onion (sliced)\n- 1 tsp Ginger-Garlic paste\n- 2 Green Chillies\n- 1/2 tsp Turmeric Powder\n- 1 tsp Red Chilli Powder\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Oil",
        "instructions": "1. Heat oil in a pan, add mustard seeds and curry leaves until they crackle.\n2. Add sliced onions and green chillies; sauté until golden brown.\n3. Add ginger-garlic paste and sauté for 1 minute until raw aroma disappears.\n4. Add chopped tomatoes, turmeric, red chilli powder, and salt. Cook on medium flame until tomatoes turn soft, pulpy, and oil separates.\n5. Add cooked rice and toss gently to combine with the tomato gravy. Serve hot with raita or potato chips!",
        "total_time": 20,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 2,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Fragrant Vegetable Biryani",
        "cleaned_ingredients": "basmati rice, carrot, potato, green pea, onion, tomato, ginger, garlic, curd, mint, coriander, biryani masala, ghee, oil, salt",
        "ingredients_raw": "- 1.5 cups Basmati Rice (soaked for 20 mins)\n- 1 Carrot (chopped)\n- 1 Potato (cubed)\n- 1/2 cup Green Peas\n- 1 large Onion (thinly sliced)\n- 1 large Tomato (chopped)\n- 1 tbsp Ginger-Garlic paste\n- 1/4 cup Curd (Yogurt)\n- 1/4 cup Mint Leaves\n- 1/4 cup Coriander Leaves\n- 1.5 tbsp Biryani Masala / Garam Masala\n- 2 tbsp Ghee & 1 tbsp Oil\n- Salt to taste",
        "instructions": "1. Heat ghee and oil in a heavy cooker/pot. Add whole spices (bay leaf, cloves, cinnamon, cardamom) and sliced onions; sauté until golden brown.\n2. Add ginger-garlic paste and sauté for 1 minute.\n3. Add tomatoes, mint, coriander, biryani masala, and curd; cook until oil separates.\n4. Add mixed vegetables (carrot, potato, peas) and sauté for 2 minutes.\n5. Add soaked drained basmati rice and 2.5 cups of water; season with salt.\n6. Cover and cook on medium-low flame for 15 minutes (or 2 whistles in cooker). Let steam release naturally. Fluff and serve with onion raita!",
        "total_time": 35,
        "meal_type": "Dinner",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Medium",
        "cuisine": "Indian",
        "cuisine_detail": "South Indian"
    },

    # ==================== CURRIES & GRAVIES ====================
    {
        "recipe_name": "Restaurant Style Paneer Butter Masala",
        "cleaned_ingredients": "paneer, butter, tomato, onion, ginger, garlic, cashew, cream, garam masala, red chilli powder, kasuri methi, salt, oil",
        "ingredients_raw": "- 200g Paneer (cubed)\n- 2 tbsp Butter & 1 tbsp Oil\n- 3 large ripe Tomatoes (pureed)\n- 1 large Onion (finely chopped)\n- 1 tbsp Ginger-Garlic paste\n- 10-12 Cashews (soaked and blended into paste)\n- 2 tbsp Fresh Cream\n- 1 tsp Kashmiri Red Chilli Powder\n- 1/2 tsp Garam Masala\n- 1 tsp Kasuri Methi (crushed)\n- Salt to taste",
        "instructions": "1. Heat 1 tbsp butter and oil in a pan. Add chopped onions and sauté until golden; add ginger-garlic paste and cook for 1 minute.\n2. Pour in tomato puree, red chilli powder, and salt. Cook covered on medium heat until oil separates from gravy.\n3. Stir in the cashew paste and 1/2 cup water; simmer for 3 minutes until rich and creamy.\n4. Gently add paneer cubes, garam masala, and kasuri methi; simmer for 2-3 minutes.\n5. Stir in fresh cream and remaining butter. Serve warm with naan, roti, or jeera rice!",
        "total_time": 25,
        "meal_type": "Dinner",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "North Indian"
    },
    {
        "recipe_name": "Homestyle Dal Tadka (Yellow Dal with Ghee Tempering)",
        "cleaned_ingredients": "toor dal, moong dal, tomato, onion, garlic, cumin, green chilli, turmeric, red chilli powder, coriander, ghee, salt",
        "ingredients_raw": "- 1/2 cup Toor Dal & 1/4 cup Yellow Moong Dal\n- 1 medium Onion (chopped)\n- 1 large Tomato (chopped)\n- 5-6 cloves Garlic (minced)\n- 1 tsp Cumin Seeds (Jeera)\n- 2 Green Chillies (slit)\n- 1/2 tsp Turmeric Powder\n- 1 tsp Red Chilli Powder\n- 2 tbsp fresh Coriander Leaves\n- 2 tbsp Ghee\n- Salt to taste",
        "instructions": "1. Pressure cook toor dal and moong dal with turmeric and 2.5 cups of water for 4 whistles until soft; mash lightly.\n2. In a pan, heat 1 tbsp ghee; add cumin seeds, chopped garlic, green chillies, and onions; sauté until golden.\n3. Add chopped tomatoes, red chilli powder, and salt; cook until tomatoes are soft.\n4. Pour in the cooked dal and 1/2 cup water; simmer on medium flame for 5 minutes.\n5. In a small pan, heat 1 tbsp ghee, add a pinch of cumin and dry red chilli for tadka; pour over the simmering dal.\n6. Garnish with coriander leaves and serve with hot basmati rice or rotis.",
        "total_time": 25,
        "meal_type": "Dinner",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "North Indian"
    },
    {
        "recipe_name": "South Indian Potato Fry (Urulaikizhangu Roast / Poriyal)",
        "cleaned_ingredients": "potato, onion, mustard, urad dal, turmeric, red chilli powder, curry leaf, salt, oil",
        "ingredients_raw": "- 3 medium Potatoes (boiled, peeled, and cubed)\n- 1 small Onion (chopped)\n- 1 tsp Mustard Seeds\n- 1 tsp Urad Dal\n- 1/2 tsp Turmeric Powder\n- 1.5 tsp Red Chilli Powder / Sambar Powder\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Oil",
        "instructions": "1. Heat oil in a heavy kadai or pan; add mustard seeds, urad dal, and curry leaves; let mustard crackle.\n2. Add chopped onions and sauté until translucent.\n3. Add boiled cubed potatoes, turmeric powder, red chilli powder, and salt.\n4. Toss well to coat all potato pieces evenly in the spices.\n5. Roast on low-medium flame for 10-12 minutes, stirring occasionally, until potatoes turn crispy and golden brown.\n6. Serve as the ultimate side dish with Sambar Rice, Rasam Rice, or Curd Rice!",
        "total_time": 20,
        "meal_type": "Lunch",
        "diet": "Vegetarian",
        "servings": 3,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "South Indian Egg Thokku / Egg Curry (Muttai Thokku)",
        "cleaned_ingredients": "egg, onion, tomato, ginger, garlic, green chilli, turmeric, red chilli powder, coriander powder, garam masala, mustard, curry leaf, salt, oil",
        "ingredients_raw": "- 4 boiled Eggs (peeled and lightly slit)\n- 2 large Onions (finely chopped)\n- 2 large Tomatoes (finely chopped)\n- 1 tbsp Ginger-Garlic paste\n- 2 Green Chillies\n- 1/2 tsp Turmeric Powder\n- 1.5 tsp Red Chilli Powder\n- 1 tsp Coriander Powder\n- 1/2 tsp Garam Masala\n- 1 tsp Mustard Seeds\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Oil",
        "instructions": "1. Heat 1 tsp oil in a pan, add a pinch of turmeric and chilli powder; roast boiled eggs for 2 minutes until lightly browned, set aside.\n2. Heat remaining oil in the same pan, crackle mustard seeds and curry leaves.\n3. Add chopped onions and green chillies; sauté until deep golden brown.\n4. Add ginger-garlic paste and cook for 1 minute; add chopped tomatoes and cook until soft and oil leaves the sides.\n5. Add turmeric, chilli powder, coriander powder, garam masala, and salt. Sauté spice paste for 2 minutes.\n6. Add 1/2 cup water, drop in the roasted eggs, and simmer on low flame for 5 minutes until gravy is thick.\n7. Garnish with coriander leaves and serve with rice, chapati, or parotta!",
        "total_time": 25,
        "meal_type": "Dinner",
        "diet": "Non-Vegetarian",
        "servings": 2,
        "difficulty": "Easy",
        "cuisine": "Indian",
        "cuisine_detail": "Tamil Nadu"
    },
    {
        "recipe_name": "Authentic Chettinad Chicken Curry",
        "cleaned_ingredients": "chicken, onion, tomato, ginger, garlic, coconut, red chilli, coriander, cumin, pepper, fennel, turmeric, curry leaf, salt, oil",
        "ingredients_raw": "- 500g Chicken (curry cut)\n- 2 medium Onions (finely chopped)\n- 2 ripe Tomatoes (chopped)\n- 1.5 tbsp Ginger-Garlic paste\n- 1/4 cup grated Coconut\n- 4-5 Dry Red Chillies\n- 1 tbsp Coriander Seeds\n- 1 tsp Cumin Seeds\n- 1.5 tsp Black Peppercorns\n- 1 tsp Fennel Seeds (Sombu)\n- 1/2 tsp Turmeric Powder\n- 1 sprig Curry Leaves\n- Salt to taste\n- 2 tbsp Sesame Oil",
        "instructions": "1. Dry roast dry red chillies, coriander seeds, cumin, black peppercorns, fennel seeds, and coconut until aromatic. Cool and grind into a smooth Chettinad masala paste with a little water.\n2. Heat sesame oil in a pot, add curry leaves and chopped onions; sauté until golden brown.\n3. Add ginger-garlic paste and sauté for 1 minute; add tomatoes and cook until soft.\n4. Add chicken pieces, turmeric powder, and salt; sauté on high heat for 3-4 minutes until chicken changes color.\n5. Add the ground Chettinad spice paste and 1 cup of water. Stir well, cover, and simmer for 15-20 minutes until chicken is tender and oil floats on top.\n6. Garnish with fresh coriander leaves. Serve hot with steamed rice, idli, or parotta!",
        "total_time": 35,
        "meal_type": "Dinner",
        "diet": "Non-Vegetarian",
        "servings": 3,
        "difficulty": "Medium",
        "cuisine": "Indian",
        "cuisine_detail": "Chettinad"
    }
]


def merge_authentic_recipes():
    print("Loading current processed_recipes.csv...")
    df = pd.read_csv(PROCESSED_CSV_PATH)
    print(f"Current total rows: {len(df)}")

    # Convert curated recipes to DataFrame
    curated_df = pd.DataFrame(AUTHENTIC_RECIPES)
    curated_df["ingredient_count"] = curated_df["cleaned_ingredients"].apply(
        lambda s: len([x for x in s.split(",") if x.strip()])
    )

    # Put curated authentic recipes at the TOP of the dataset!
    combined_df = pd.concat([curated_df, df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["recipe_name"])

    combined_df.to_csv(PROCESSED_CSV_PATH, index=False, encoding="utf-8")
    print(f"Successfully added {len(curated_df)} authentic Indian recipes!")
    print(f"New total recipes count: {len(combined_df)}")


if __name__ == "__main__":
    merge_authentic_recipes()
