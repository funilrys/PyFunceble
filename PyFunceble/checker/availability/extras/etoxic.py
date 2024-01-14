"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler for the etoxic infrastructure.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase


class EToxicHandler(ExtraRuleHandlerBase):
    """
    Provides our very own rulesets for the etoxic infrastructure.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    MATCHES = [
        ".0wn0.com",
        ".123.st",
        ".1forum.biz",
        ".1fr1.net",
        ".1talk.net",
        ".30yearsstillyoung.com",
        ".3oloum.com",
        ".3rab.pro",
        ".4umer.com",
        ".5turbo.org",
        ".666forum.com",
        ".7olm.org",
        ".ace.st",
        ".actieforum.com",
        ".actifforum.com",
        ".aforumfree.com",
        ".africamotion.net",
        ".ahladalil.com",
        ".ahlamontada.com",
        ".ahlamontada.net",
        ".ahlamountada.com",
        ".airesdelibertad.com",
        ".alanoblebouffarde.com",
        ".aldeiarpg.com",
        ".all-up.com",
        ".ambiance-varadero.com",
        ".amoticos.org",
        ".arabepro.com",
        ".archeryonline.net",
        ".argyletd.com",
        ".artes-ana.com",
        ".audittpassion.com",
        ".avenir-vsp.com",
        ".bachandbachettefans.net",
        ".banouta.net",
        ".bbactif.com",
        ".beagle-attitude.com",
        ".benimforum.net",
        ".black-librarium.com",
        ".boxster-cayman.com",
        ".briefmarken-forum.com",
        ".bromptonforum.net",
        ".caferacerclub.org",
        ".camperfree.com",
        ".canadaboard.net",
        ".canadian-forum.com",
        ".cantal-leforum.com",
        ".casatridente.com",
        ".catsboard.com",
        ".cdnmilitarycollectors.com",
        ".chemin-de-memoire-parachutistes.org",
        ".clooneysopenhouse.com",
        ".club-bajaj.com",
        ".clubcb500x.com",
        ".clubgtipowers.com",
        ".clubtrackerarg.com",
        ".contrabaixobr.com",
        ".corvettepassion.com",
        ".coxengineforum.com",
        ".cro-wood.com",
        ".dan-moc.net",
        ".darkbb.com",
        ".deco-moderne-fr.com",
        ".desforums.net",
        ".detenteaujardin.com",
        ".discustoutsimplement.com",
        ".e30passion.com",
        ".easyforumpro.com",
        ".editboard.com",
        ".enbicielectrica.com",
        ".entreelles.org",
        ".exprimetoi.net",
        ".fcmulhousefans.com",
        ".filthy-secret.com",
        ".fmsp.net",
        ".focusrstteam.com",
        ".ford100e.org",
        ".foroactivo.com",
        ".foroactivo.com.es",
        ".forseps.org",
        ".forum-jardins.com",
        ".forum-zafira.com",
        ".forum2jeux.com",
        ".forumactif.com",
        ".forumactif.fr",
        ".forumactif.org",
        ".forumalgerie.net",
        ".forumattivo.it",
        ".forumbrasil.net",
        ".forumegypt.net",
        ".forumeiros.com",
        ".forumeiros.net",
        ".forumgamers.net",
        ".forumgaming.fr",
        ".forumgratuit.be",
        ".forumgratuit.ch",
        ".forumgratuit.org",
        ".forumgratuit.ro",
        ".forumgreek.com",
        ".forumgsr750.com",
        ".forumlaguna3.com",
        ".forumlumix.com",
        ".forumotion.com",
        ".forumotion.net",
        ".forumperso.com",
        ".forumpro.fr",
        ".forums-actifs.com",
        ".forumshiba.com",
        ".forumvi.com",
        ".fra.co",
        ".fritzbox-forum.com",
        ".fxsforexsrbijaforum.com",
        ".galoppourlavie.org",
        ".gid3an.com",
        ".giocattolivintage.com",
        ".glory-box-forum.com",
        ".goldwingpartage.com",
        ".goodforum.net",
        ".grisoghetto.com",
        ".gunetwork.org",
        ".hareketforum.net",
        ".hifi4sale.net",
        ".hooxs.com",
        ".i-love-harvard.com",
        ".iftopic.com",
        ".imperialgunneryforum.com",
        ".jeun.fr",
        ".jordanforum.net",
        ".just-married-rpg.com",
        ".kanak.fr",
        ".kawasaki-customs-forum.com",
        ".keuf.net",
        ".la-taverne-des-aventuriers.com",
        ".le-medaillon.org",
        ".le-site-de-la-citroen-xm.com",
        ".lebonforum.com",
        ".leforumlafigurine.com",
        ".legion-etrangere-munch.com",
        ".lemondedudiagauto.com",
        ".letrasyalgomas.com",
        ".levriers-forever.com",
        ".lights-camera-action.org",
        ".longluntan.com",
        ".magic-tarot58.com",
        ".mam9.com",
        ".manager-fifa.com",
        ".marvelscustoms.net",
        ".materielceleste.com",
        ".matostt.com",
        ".megane4forum.com",
        ".meilleurforum.com",
        ".minivanchrysler.com",
        ".mirbb.com",
        ".misteria7.com",
        ".montres-russes.org",
        ".moseisleyraumhafen.com",
        ".mundoqashqai.com",
        ".never-utopia.com",
        ".niceboard.com",
        ".novaerarpg.com",
        ".obd2sos.net",
        ".onepiece-mangas.com",
        ".open-consoles.com",
        ".orizzontescuolaforum.net",
        ".ottobreaddicts.net",
        ".own0.com",
        ".palstani.com",
        ".passion-harley.net",
        ".passionmilitaria.com",
        ".passionphoto-passionmontage.com",
        ".pblvfrance3.com",
        ".photos-camions.com",
        ".planete4x4.com",
        ".portalmercedes.com",
        ".portalmercedesbrasil.com",
        ".pro-forum.fr",
        ".puntoevoforum.com",
        ".quilterslastresort.com",
        ".repartocorse2.com",
        ".rigala.net",
        ".roo7.biz",
        ".rpg-board.net",
        ".rpghogwarts.org",
        ".sanata.biz",
        ".sdvg-deti.com",
        ".serbianforum.info",
        ".sgt3r.com",
        ".shaveua.com",
        ".sheffieldboardgamers.com",
        ".small-tracks.org",
        ".sorcieremonique.com",
        ".sporepedia2.com",
        ".stickeristas.com",
        ".subarashiis.com",
        ".superforo.net",
        ".superforum.fr",
        ".suzuki800.com",
        ".syriaforums.net",
        ".t5zone.com",
        ".team-z1000.com",
        ".terre-bitume.org",
        ".tibiaface.com",
        ".tubelesskite.net",
        ".ufologie-paranormal.org",
        ".unimog-mania.com",
        ".v2-honda.com",
        ".velovintageagogo.com",
        ".viterbikers.com",
        ".vivelecrpe.com",
        ".vstromhellasforum.com",
        ".walkingdead-rpg.com",
        ".warriorcatsnl.com",
        ".warriors-rpg.com",
        ".wwrail.net",
        ".yoo7.com",
        ".ze-43eme.com",
        ".zxr7team.com",
    ]

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "EToxicHandler":
        PyFunceble.facility.Logger.info(
            "Started to check %r against the eToxic handler.",
            self.status.idna_subject,
        )

        if self.status.status_before_extra_rules == PyFunceble.storage.STATUS.up:
            if any(self.status.netloc.endswith(x) for x in self.MATCHES):
                self.do_on_header_match(
                    self.req_url,
                    matches={"location": [f"/{self.status.netloc}", "/search/"]},
                    method=self.switch_to_down,
                    allow_redirects=False,
                    match_mode="std",
                    strict=True,
                )

        PyFunceble.facility.Logger.info(
            "Finished to check %r against our the eToxic handler.",
            self.status.idna_subject,
        )

        return self
