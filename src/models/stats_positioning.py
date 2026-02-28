class StatsPositioning:
    """
    Représente les statistiques de positionnement d'un joueur pour une
    participation à un match.
    """

    def __init__(
        self,
        participation_id: int = 0,
        average_distance_to_ball: int = 0,
        # average_distance_to_ball_possession: int = 0,
        # average_distance_to_ball_no_possession: int = 0,
        average_distance_to_mates: int = 0,
        time_defensive_third: float = 0.0,
        time_neutral_third: float = 0.0,
        time_offensive_third: float = 0.0,
        # time_defensive_half: float = 0.0,
        # time_offensive_half: float = 0.0,
        time_behind_ball: float = 0.0,
        time_infront_ball: float = 0.0,
        time_most_back: float = 0.0,
        time_most_forward: float = 0.0,
        goals_against_while_last_defender: int = 0,
        time_closest_to_ball: float = 0.0,
        time_farthest_to_ball: float = 0.0,
        percent_defensive_third: float = 0.0,
        percent_neutral_third: float = 0.0,
        percent_offensive_third: float = 0.0,
        percent_defensive_half: float = 0.0,
        percent_offensive_half: float = 0.0,
        percent_behind_ball: float = 0.0,
        percent_infront_ball: float = 0.0,
        percent_most_back: float = 0.0,
        percent_most_forward: float = 0.0,
        percent_closest_to_ball: float = 0.0,
        percent_farthest_from_ball: float = 0.0,
    ):
        """
        Initialise les statistiques de positionnement.

        Parameters
        ----------
        participation_id : int, optional
            Identifiant de la participation au match, par défaut 0.
        average_distance_to_ball : int, optional
            Distance moyenne du joueur par rapport à la balle en unités de jeu,
            par défaut 0.
        average_distance_to_ball_possession : int, optional
            Distance moyenne à la balle lorsque l'équipe est en possession,
            par défaut 0. (non utilisé)
        average_distance_to_ball_no_possession : int, optional
            Distance moyenne à la balle lorsque l'équipe n'est pas en possession,
            par défaut 0. (non utilisé)
        average_distance_to_mates : int, optional
            Distance moyenne du joueur par rapport à ses coéquipiers, par défaut 0.
        time_defensive_third : float, optional
            Temps passé dans le tiers défensif en secondes, par défaut 0.0.
        time_neutral_third : float, optional
            Temps passé dans le tiers neutre en secondes, par défaut 0.0.
        time_offensive_third : float, optional
            Temps passé dans le tiers offensif en secondes, par défaut 0.0.
        time_defensive_half : float, optional
            Temps passé dans la moitié défensive en secondes, par défaut 0.0.
        time_offensive_half : float, optional
            Temps passé dans la moitié offensive en secondes, par défaut 0.0.
        time_behind_ball : float, optional
            Temps passé derrière la balle en secondes, par défaut 0.0.
        time_infront_ball : float, optional
            Temps passé devant la balle en secondes, par défaut 0.0.
        time_most_back : float, optional
            Temps passé en position la plus reculée de l'équipe en secondes,
            par défaut 0.0.
        time_most_forward : float, optional
            Temps passé en position la plus avancée de l'équipe en secondes,
            par défaut 0.0.
        goals_against_while_last_defender : int, optional
            Nombre de buts encaissés alors que le joueur était le dernier
            défenseur, par défaut 0.
        time_closest_to_ball : float, optional
            Temps passé comme joueur le plus proche de la balle en secondes,
            par défaut 0.0.
        time_farthest_to_ball : float, optional
            Temps passé comme joueur le plus éloigné de la balle en secondes,
            par défaut 0.0.
        percent_defensive_third : float, optional
            Pourcentage du match passé dans le tiers défensif, par défaut 0.0.
        percent_neutral_third : float, optional
            Pourcentage du match passé dans le tiers neutre, par défaut 0.0.
        percent_offensive_third : float, optional
            Pourcentage du match passé dans le tiers offensif, par défaut 0.0.
        percent_defensive_half : float, optional
            Pourcentage du match passé dans la moitié défensive, par défaut 0.0.
        percent_offensive_half : float, optional
            Pourcentage du match passé dans la moitié offensive, par défaut 0.0.
        percent_behind_ball : float, optional
            Pourcentage du match passé derrière la balle, par défaut 0.0.
        percent_infront_ball : float, optional
            Pourcentage du match passé devant la balle, par défaut 0.0.
        percent_most_back : float, optional
            Pourcentage du match passé en position la plus reculée, par défaut 0.0.
        percent_most_forward : float, optional
            Pourcentage du match passé en position la plus avancée, par défaut 0.0.
        percent_closest_to_ball : float, optional
            Pourcentage du match passé comme joueur le plus proche de la balle,
            par défaut 0.0.
        percent_farthest_from_ball : float, optional
            Pourcentage du match passé comme joueur le plus éloigné de la balle,
            par défaut 0.0.
        """

        self._participation_id = participation_id
        self.average_distance_to_ball = average_distance_to_ball
        # self.average_distance_to_ball_possession = average_distance_to_ball_possession,
        # self.average_distance_to_ball_no_possession = average_distance_to_ball_no_possession,
        self.average_distance_to_mates = average_distance_to_mates
        self.time_defensive_third = time_defensive_third
        self.time_neutral_third = time_neutral_third
        self.time_offensive_third = time_offensive_third
        # self.time_defensive_half = time_defensive_half
        # self.time_offensive_half = time_offensive_half
        self.time_behind_ball = time_behind_ball
        self.time_infront_ball = time_infront_ball
        self.time_most_back = time_most_back
        self.time_most_forward = time_most_forward
        self.goals_against_while_last_defender = goals_against_while_last_defender
        self.time_closest_to_ball = time_closest_to_ball
        self.time_farthest_to_ball = time_farthest_to_ball
        self.percent_defensive_third = percent_defensive_third
        self.percent_neutral_third = percent_neutral_third
        self.percent_offensive_third = percent_offensive_third
        self.percent_defensive_half = percent_defensive_half
        self.percent_offensive_half = percent_offensive_half
        self.percent_behind_ball = percent_behind_ball
        self.percent_infront_ball = percent_infront_ball
        self.percent_most_back = percent_most_back
        self.percent_most_forward = percent_most_forward
        self.percent_closest_to_ball = percent_closest_to_ball
        self.percent_farthest_from_ball = percent_farthest_from_ball
