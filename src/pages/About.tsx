import React from "react";
import { ButtonItem, Navigation, PanelSectionRow } from "@decky/ui";
import { FaExternalLinkAlt, FaGithubAlt } from "react-icons/fa";

export const About = () => {
  return (
    <>
      <h2
        style={{ fontWeight: "bold", fontSize: "1.5em", marginBottom: "0px" }}
      >
        Read Deck For Me
      </h2>
      <span>
        A Decky plugin to read the screen for you.
        <br />
      </span>
      <PanelSectionRow>
        <ButtonItem
          icon={<FaGithubAlt style={{ display: "block" }} />}
          label="Read Deck For Me"
          onClick={() => {
            Navigation.NavigateToExternalWeb(
              "https://github.com/szhshp/Decky-ReadDeckForMe"
            );
          }}
        >
          GitHub Repo
        </ButtonItem>
      </PanelSectionRow>

      <h2
        style={{ fontWeight: "bold", fontSize: "1.5em", marginBottom: "0px" }}
      >
        Developer
      </h2>
      <PanelSectionRow>
        <ButtonItem
          icon={<FaExternalLinkAlt style={{ display: "block" }} />}
          label="szhshp"
          onClick={() => {
            Navigation.NavigateToExternalWeb("https://szhshp.org/");
          }}
        >
          Steam Profile
        </ButtonItem>
      </PanelSectionRow>

      <h2
        style={{ fontWeight: "bold", fontSize: "1.5em", marginBottom: "0px" }}
      >
        Support
      </h2>
      <span>
        Log an issue on GitHub to report bugs or request features.
        <br />
      </span>
      <PanelSectionRow>
        <ButtonItem
          icon={<FaGithubAlt style={{ display: "block" }} />}
          label="@steamdecktalk"
          onClick={() => {
            Navigation.NavigateToExternalWeb(
              "https://github.com/szhshp/Decky-ReadDeckForMe/issues"
            );
          }}
        >
          Telegram Group
        </ButtonItem>
      </PanelSectionRow>
    </>
  );
};
