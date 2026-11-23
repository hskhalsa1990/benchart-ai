package components

import androidx.compose.runtime.Composable
import org.jetbrains.compose.web.attributes.ButtonType
import org.jetbrains.compose.web.attributes.type
import org.jetbrains.compose.web.css.marginLeft
import org.jetbrains.compose.web.css.px
import org.jetbrains.compose.web.dom.*

@Composable
fun AutoGroup(
    isEnabled: Boolean,
    onButtonClicked: () -> Unit
) {
    Div(
        attrs = {
            classes("form-group")
            style {
                marginLeft(10.px)
            }
        }
    ) {
        // 🖌 Color map

        Label(
            forId = "colorMap",
            attrs = {
                classes("form-label")
            }
        ) {
            Text("Auto Group:")
        }
        Br()
        Button(
            attrs = {
                id("colorMap")
                classes("btn", if (isEnabled) "btn-success" else "btn-secondary")
                onClick {
                    onButtonClicked()
                }
                type(ButtonType.Button)
            }
        ) {
            Text(if (isEnabled) "ON" else "OFF")
        }
    }
}