"""
RED PHASE: Tests for Complete End-to-End User Workflows
These tests MUST FAIL before implementation exists.
NO MOCKING ALLOWED - Tests will use real complete system workflows.
"""

from __future__ import annotations

import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestCompleteUserWorkflows:
    """Test that complete end-to-end user workflows work correctly."""

    @pytest.fixture(scope="class")
    def setup_complete_system(self) -> None:
        """Start complete system (backend + frontend + database)."""
        # Start backend server
        self.backend_process = subprocess.Popen(
            [
                "python",
                "-m",
                "uvicorn",
                "todowrite_web.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            cwd="web_package/backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(3)

        # Start frontend server
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="web_package/frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        time.sleep(5)

        yield

        # Clean up
        self.backend_process.terminate()
        self.frontend_process.terminate()
        self.backend_process.wait(timeout=5)
        self.frontend_process.wait(timeout=5)

    @pytest.fixture(scope="class")
    def setup_web_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver for E2E testing."""
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver: webdriver.Chrome = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_new_user_complete_onboarding_journey(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete new user onboarding journey."""
        driver: webdriver.Chrome = setup_web_driver

        # Step 1: User visits homepage
        driver.get("http://localhost:3000")
        assert "ToDoWrite" in driver.title, "Should load homepage"

        # Step 2: User clicks Get Started
        get_started = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='get-started-button']"
        )
        get_started.click()

        # Step 3: User selects template
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='template-selection']")
            )
        )

        vacation_template = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Plan Vacation')]"
        )
        vacation_template.click()

        # Step 4: User customizes template
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='template-customization']")
            )
        )

        destination_input = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='destination-field']"
        )
        destination_input.send_keys("Hawaii")

        dates_input = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='travel-dates-field']"
        )
        dates_input.send_keys("2024-06-01 to 2024-06-15")

        # Step 5: User reviews and creates project
        next_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='next-step-button']"
        )
        next_button.click()

        create_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='create-project-button']"
        )
        create_button.click()

        # Step 6: User views created project
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='project-dashboard']")
            )
        )

        project_title = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='project-title']"
        )
        assert (
            "Hawaii Vacation" in project_title.text
        ), "Project should show custom title"

        # Step 7: User adds first action item
        add_item_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='add-action-item-button']"
        )
        add_item_button.click()

        item_input = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='action-item-input']"
        )
        item_input.send_keys("Book flights to Honolulu")

        save_item_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='save-action-button']"
        )
        save_item_button.click()

        # Verify complete journey success
        created_item = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Book flights to Honolulu')]"
        )
        assert (
            created_item.is_displayed()
        ), "Created action item should be visible"

    def test_template_based_project_complete_workflow(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete template-based project workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Navigate to templates
        driver.get("http://localhost:3000/templates")

        # Browse categories
        categories = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='template-category']"
        )
        assert len(categories) > 0, "Should show template categories"

        # Select Home Organization category
        home_org_category = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Home Organization')]"
        )
        home_org_category.click()

        # Select Clean Closet template
        closet_template = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Clean Closet')]"
        )
        closet_template.click()

        # Preview template
        preview = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='template-preview']"
        )
        assert preview.is_displayed(), "Should show template preview"

        # Customize with personal details
        customize_button = preview.find_element(
            By.CSS_SELECTOR, "[data-testid='customize-template-button']"
        )
        customize_button.click()

        # Add customization details
        room_size = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='room-size-field']"
        )
        room_size.send_keys("Medium")

        timeframe = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='timeframe-field']"
        )
        timeframe.send_keys("2 weekends")

        # Generate project structure
        generate_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='generate-structure-button']"
        )
        generate_button.click()

        # Review generated structure
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='structure-review']")
            )
        )

        # Customize generated items
        add_custom_item = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='add-custom-item-button']"
        )
        add_custom_item.click()

        custom_item_input = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='custom-item-input']"
        )
        custom_item_input.send_keys("Buy matching hangers and containers")

        # Create final project
        create_project = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='create-final-project-button']"
        )
        create_project.click()

        # Verify complete workflow
        dashboard = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='project-dashboard']"
        )
        assert dashboard.is_displayed(), "Should land on project dashboard"

        project_items = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='project-item']"
        )
        assert len(project_items) > 0, "Should show project items"

    def test_visual_relationship_building_complete_workflow(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete visual relationship building workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Navigate to existing project
        driver.get("http://localhost:3000/projects/closet-project")

        # Enable relationship view
        relationship_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='relationship-view-button']"
        )
        relationship_button.click()

        # Create first relationship via drag-and-drop
        source_item = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='draggable-item']:first-child"
        )
        target_item = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='draggable-item']:nth-child(2)"
        )

        actions = ActionChains(driver)
        actions.drag_and_drop(source_item, target_item).perform()

        # Select relationship type
        relationship_popup = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='relationship-popup']"
        )
        depends_on_option = relationship_popup.find_element(
            By.XPATH, "//*[contains(text(), 'Must finish before')]"
        )
        depends_on_option.click()

        save_relationship = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='save-relationship-button']"
        )
        save_relationship.click()

        # Verify visual connection
        connection_line = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='connection-line']"
        )
        assert (
            connection_line.is_displayed()
        ), "Visual connection should appear"

        # View dependency tree
        tree_view_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='tree-view-button']"
        )
        tree_view_button.click()

        dependency_tree = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='dependency-tree']"
        )
        assert (
            dependency_tree.is_displayed()
        ), "Dependency tree should be visible"

        # Test circular dependency detection
        # Try to create circular relationship
        actions.drag_and_drop(target_item, source_item).perform()

        # Should show warning
        warning = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='circular-dependency-warning']"
        )
        assert warning.is_displayed(), "Should detect circular dependency"

        cancel_relationship = warning.find_element(
            By.CSS_SELECTOR, "[data-testid='cancel-relationship-button']"
        )
        cancel_relationship.click()

    def test_search_and_discovery_complete_workflow(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete search and discovery workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Navigate to projects list
        driver.get("http://localhost:3000/projects")

        # Perform natural language search
        search_bar = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='search-bar']"
        )
        search_bar.send_keys("vacation packing")

        search_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='search-button']"
        )
        search_button.click()

        # Verify search results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='search-results']")
            )
        )

        search_results = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='search-result-item']"
        )
        assert len(search_results) > 0, "Should show search results"

        # Test advanced filtering
        advanced_search = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='advanced-search-button']"
        )
        advanced_search.click()

        # Add filters
        status_filter = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='status-filter']"
        )
        status_filter.send_keys("In Progress")

        date_filter = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='date-filter']"
        )
        date_filter.send_keys("Last 30 days")

        apply_filters = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='apply-filters-button']"
        )
        apply_filters.click()

        # Verify filtered results
        filtered_results = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='filtered-result-item']"
        )
        assert len(filtered_results) > 0, "Should show filtered results"

        # Save search query
        save_search = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='save-search-button']"
        )
        save_search.click()

        search_name = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='search-name-input']"
        )
        search_name.send_keys("My Vacation Search")

        confirm_save = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='confirm-save-search']"
        )
        confirm_save.click()

        # Verify saved search appears in sidebar
        saved_searches = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='saved-searches']"
        )
        assert (
            "My Vacation Search" in saved_searches.text
        ), "Saved search should appear in sidebar"

    def test_data_import_export_complete_workflow(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete data import/export workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Navigate to project with data
        driver.get("http://localhost:3000/projects/sample-project")

        # Export project as YAML
        export_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='export-button']"
        )
        export_button.click()

        format_options = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='format-options']"
        )
        yaml_option = format_options.find_element(
            By.XPATH, "//*[contains(text(), 'YAML')]"
        )
        yaml_option.click()

        include_completed = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='include-completed-checkbox']"
        )
        include_completed.click()  # Exclude completed items

        confirm_export = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='confirm-export-button']"
        )
        confirm_export.click()

        # Wait for download to complete
        time.sleep(3)

        # Verify download link appears
        download_link = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='download-link']"
        )
        assert download_link.is_displayed(), "Download link should appear"

        # Test import functionality
        import_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='import-button']"
        )
        import_button.click()

        # Simulate file upload (would need file input)
        # For now, test that import dialog appears
        import_dialog = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='import-dialog']"
        )
        assert import_dialog.is_displayed(), "Import dialog should appear"

        # Test conflict resolution
        simulate_conflict = import_dialog.find_element(
            By.CSS_SELECTOR, "[data-testid='simulate-conflict-button']"
        )
        simulate_conflict.click()

        conflict_resolution = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='conflict-resolution']"
        )
        assert (
            conflict_resolution.is_displayed()
        ), "Should show conflict resolution options"

        # Choose merge option
        merge_option = conflict_resolution.find_element(
            By.CSS_SELECTOR, "[data-testid='merge-option']"
        )
        merge_option.click()

        confirm_import = import_dialog.find_element(
            By.CSS_SELECTOR, "[data-testid='confirm-import-button']"
        )
        confirm_import.click()

        # Verify import completion
        success_message = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='import-success-message']"
        )
        assert (
            success_message.is_displayed()
        ), "Should show import success message"

    def test_team_collaboration_complete_workflow(
        self, setup_web_driver: webdriver.Chrome, setup_complete_system: None
    ) -> None:
        """RED: Test complete team collaboration workflow."""
        driver: webdriver.Chrome = setup_web_driver

        # Navigate to project
        driver.get("http://localhost:3000/projects/team-project")

        # Share project with team
        share_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='share-project-button']"
        )
        share_button.click()

        # Add team member
        invite_modal = driver.find_element(
            By.CssSelector, "[data-testid='invite-modal']"
        )
        email_input = invite_modal.find_element(
            By.CSS_SELECTOR, "[data-testid='email-input']"
        )
        email_input.send_keys("team@example.com")

        permission_select = invite_modal.find_element(
            By.CSS_SELECTOR, "[data-testid='permission-select']"
        )
        permission_select.send_keys("Editor")

        send_invite = invite_modal.find_element(
            By.CSS_SELECTOR, "[data-testid='send-invite-button']"
        )
        send_invite.click()

        # Wait for team member to join
        time.sleep(2)

        # Assign task to team member
        task_item = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='task-item']:first-child"
        )
        task_item.click()

        assign_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='assign-button']"
        )
        assign_button.click()

        team_member_option = driver.find_element(
            By.XPATH, "//*[contains(text(), 'team@example.com')]"
        )
        team_member_option.click()

        confirm_assignment = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='confirm-assignment-button']"
        )
        confirm_assignment.click()

        # Add comment for collaboration
        comment_button = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='add-comment-button']"
        )
        comment_button.click()

        comment_input = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='comment-input']"
        )
        comment_input.send_keys(
            "This task depends on the research phase being completed."
        )

        save_comment = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='save-comment-button']"
        )
        save_comment.click()

        # Verify team collaboration features
        comments_section = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='comments-section']"
        )
        assert comments_section.is_displayed(), "Comments should be visible"

        assignment_badge = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='assignment-badge']"
        )
        assert assignment_badge.is_displayed(), "Assignment should be visible"

        # Test real-time updates simulation
        update_indicator = driver.find_element(
            By.CSS_SELECTOR, "[data-testid='live-update-indicator']"
        )
        assert (
            update_indicator.is_displayed()
        ), "Should show real-time updates indicator"
