package components

import androidx.compose.runtime.Composable
import org.jetbrains.compose.web.attributes.selected
import org.jetbrains.compose.web.dom.*


@Composable
fun TestNames(
    testNames: List<String>,
    currentTestName: String? = null,
    onTestNameSelected: (option: String) -> Unit
){
    if(testNames.isNotEmpty()){
        Div(
            attrs = {
                classes("form-group")
            }
        ) {
            Label(
                forId = "testNames",
                attrs = {
                    classes("form-label")
                }
            ) {
                Text("Test Name :")
            }
            Select(
                attrs = {
                    classes("form-select")
                    id("testNames")
                    onInput {
                        it.value?.let { newTestName ->
                            onTestNameSelected(newTestName)
                        }
                    }
                }
            ) {
                for (testName in testNames) {
                    Option(
                        value = testName,
                        attrs = {
                            if (testName == currentTestName) {
                                selected()
                            }
                        }
                    ) {
                        Text(testName)
                    }
                }
            }
        }
    }
}