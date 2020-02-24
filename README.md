Le dossier model contient le code de l'automate cellulaire.
Cell_Environment.py définit les différents objets du reinforcement learning (actions, rewards, observations, ...)
en fonction de différentes parties de l'automate cellulaire.
main.py lance l'entrainement des neural networks en utilisant deer.


Model c++ : python3 setup.py install --user dans model_cpp/
Deer : remove original deer
pip install -r requirements.txt
python3 setup.py develop