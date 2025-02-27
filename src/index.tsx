/* eslint-disable react/react-in-jsx-scope */
import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
} from "@decky/ui";
import {
  addEventListener,
  removeEventListener,
  callable,
  definePlugin,
  toaster,
  // routerHook
} from "@decky/api";
import { useState } from "react";
import { FaFolder, FaShip, FaTrashAlt, FaVolumeUp } from "react-icons/fa";

const ocr_latest = callable<[], { status: string; output: string }>(
  "ocr_latest"
);
const get_latest = callable<
  [],
  { status: string; output: string; base64: string }
>("get_latest");
const delete_latest = callable<[], { status: string; output: string }>(
  "delete_latest"
);

function Content() {
  const [content, setContent] = useState<string | undefined>();
  const [loading, setLoading] = useState<boolean>(false);

  const get_latest_img = async () => {
    setLoading(true);
    const result = await get_latest();
    setContent(result.base64);
    setLoading(false);
  };

  const ocr = async () => {
    console.log("ocr");
    setLoading(true);
    await ocr_latest();
    setLoading(false);
  };

  const delete_latest_img = async () => {
    setLoading(true);
    const result = await delete_latest();
    console.log(result);
    setContent(undefined);
    setLoading(false);
  };

  return (
    <PanelSection title="Panel Section">
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={get_latest_img} disabled={loading}>
          <FaFolder style={{ paddingRight: "4px" }} />
          {loading ? "Loading..." : "Get Latest File"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={ocr} disabled={loading}>
          <FaVolumeUp style={{ paddingRight: "4px" }} />
          {loading ? "Loading..." : "Read It For Me"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={delete_latest_img}
          disabled={loading}
        >
          <FaTrashAlt style={{ paddingRight: "4px" }} />
          {loading ? "Loading..." : "Delete Latest File"}
        </ButtonItem>
      </PanelSectionRow>

      {content && (
        <PanelSectionRow>
          <div style={{ display: "flex", justifyContent: "center" }}>
            <img
              src={`data:image/png;base64,${content}`}
              alt="OCR Result"
              style={{ width: "80vw", border: "1px solid grey" }}
            />
          </div>
        </PanelSectionRow>
      )}

      {/* <PanelSectionRow>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <img src={logo} />
        </div>
      </PanelSectionRow> */}

      {/*<PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={() => {
            Navigation.Navigate("/decky-plugin-test");
            Navigation.CloseSideMenus();
          }}
        >
          Router
        </ButtonItem>
      </PanelSectionRow>*/}
    </PanelSection>
  );
}

export default definePlugin(() => {
  console.log(
    "Template plugin initializing, this is called once on frontend startup"
  );

  // serverApi.routerHook.addRoute("/decky-plugin-test", DeckyPluginRouterTest, {
  //   exact: true,
  // });

  // Add an event listener to the "timer_event" event from the backend
  const listener = addEventListener<
    [test1: string, test2: boolean, test3: number]
  >("timer_event", (test1, test2, test3) => {
    console.log("Template got timer_event with:", test1, test2, test3);
    toaster.toast({
      title: "template got timer_event",
      body: `${test1}, ${test2}, ${test3}`,
    });
  });

  return {
    // The name shown in various decky menus
    name: "Test Plugin",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>Decky Example Plugin</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <FaShip />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("Unloading");
      removeEventListener("timer_event", listener);
      // serverApi.routerHook.removeRoute("/decky-plugin-test");
    },
  };
});
